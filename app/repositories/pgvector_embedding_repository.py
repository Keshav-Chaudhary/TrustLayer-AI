import json
import math
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import settings
from app.repositories.base import BaseEmbeddingRepository
from app.repositories.db_schema import Base, EmbeddingDocumentModel

class PgVectorEmbeddingRepository(BaseEmbeddingRepository):
    def __init__(self, db_url: Optional[str] = None, session: Optional[Session] = None):
        self.db_url = db_url or settings.DATABASE_URL or "sqlite:///:memory:"
        if session:
            self.session_factory = None
            self._external_session = session
        else:
            self._external_session = None
            self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {})
            Base.metadata.create_all(self.engine)
            self.session_factory = sessionmaker(bind=self.engine)

        self._encoder = None

    def _get_encoder(self):
        if self._encoder is None:
            self._encoder = SentenceTransformer(settings.EMBEDDING_MODEL)
        return self._encoder

    def _get_session(self) -> Session:
        if self._external_session:
            return self._external_session
        return self.session_factory()

    def count(self) -> int:
        session = self._get_session()
        try:
            return session.query(EmbeddingDocumentModel).count()
        finally:
            if not self._external_session:
                session.close()

    def query_vectors(
        self,
        query_texts: List[str],
        n_results: int,
        where_clause: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        session = self._get_session()
        try:
            if isinstance(query_texts, str):
                query_texts = [query_texts]
            encoder = self._get_encoder()
            query_embeddings = encoder.encode(query_texts).tolist()

            all_docs = session.query(EmbeddingDocumentModel).all()
            if not all_docs:
                return {
                    "ids": [[] for _ in query_texts],
                    "distances": [[] for _ in query_texts],
                    "documents": [[] for _ in query_texts],
                    "metadatas": [[] for _ in query_texts]
                }

            out_ids, out_dists, out_docs, out_metas = [], [], [], []

            for q_emb in query_embeddings:
                scored_docs = []
                for doc in all_docs:
                    # Parse metadata filters if provided
                    if where_clause and "hotel_id" in where_clause:
                        if doc.hotel_id != where_clause["hotel_id"]:
                            continue

                    doc_emb = json.loads(doc.embedding_vector)
                    # Cosine distance computation
                    dot = sum(a * b for a, b in zip(q_emb, doc_emb))
                    norm_q = math.sqrt(sum(a * a for a in q_emb))
                    norm_d = math.sqrt(sum(b * b for b in doc_emb))
                    sim = dot / (norm_q * norm_d + 1e-9)
                    dist = float(1.0 - sim)

                    scored_docs.append((dist, doc))

                scored_docs.sort(key=lambda x: x[0])
                top = scored_docs[:n_results]

                out_ids.append([t[1].chunk_id for t in top])
                out_dists.append([t[0] for t in top])
                out_docs.append([t[1].snippet for t in top])
                out_metas.append([
                    {
                        "hotel_id": t[1].hotel_id,
                        "chunk_id": t[1].chunk_id,
                        "chunk_type": t[1].chunk_type,
                        "content_hash": t[1].content_hash
                    } for t in top
                ])

            return {
                "ids": out_ids,
                "distances": out_dists,
                "documents": out_docs,
                "metadatas": out_metas
            }
        finally:
            if not self._external_session:
                session.close()

    def upsert_embeddings(self, chunks: List[Dict[str, Any]]) -> int:
        session = self._get_session()
        encoder = self._get_encoder()
        count = 0
        try:
            for chk in chunks:
                cid = chk["chunk_id"]
                snippet = chk.get("snippet", "")
                chash = chk.get("content_hash", "hash")

                existing = session.query(EmbeddingDocumentModel).filter(EmbeddingDocumentModel.chunk_id == cid).first()

                if existing and existing.content_hash == chash:
                    continue  # Unchanged - skip re-embedding

                vec = encoder.encode([snippet])[0].tolist()
                vec_str = json.dumps(vec)

                if not existing:
                    existing = EmbeddingDocumentModel(
                        chunk_id=cid,
                        hotel_id=chk.get("hotel_id", ""),
                        chunk_type=chk.get("chunk_type", "Chunk A (Profile)")
                    )
                    session.add(existing)

                existing.snippet = snippet
                existing.content_hash = chash
                existing.embedding_vector = vec_str
                existing.embedding_dimension = len(vec)
                count += 1

            if not self._external_session:
                session.commit()
            return count
        except Exception:
            if not self._external_session:
                session.rollback()
            raise
        finally:
            if not self._external_session:
                session.close()
