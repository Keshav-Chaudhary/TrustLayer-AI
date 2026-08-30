import os
import chromadb
import logging
from typing import List, Dict, Any, Optional
from app.repositories.base import BaseEmbeddingRepository
from app.config.config import settings

logger = logging.getLogger("trustlayer")

class ChromaEmbeddingRepository(BaseEmbeddingRepository):
    """
    ChromaDB vector store storage adapter encapsulating PersistentClient connection,
    collection queries, and metadata retrieval.
    """
    def __init__(self, vector_dir: Optional[str] = None, collection_name: str = "hotel_knowledge"):
        self.vector_dir = vector_dir or settings.VECTOR_STORE_PATH
        resolved_path = os.path.abspath(self.vector_dir)
        if not os.path.exists(resolved_path):
            raise RuntimeError(f"ChromaDB vector store path missing at {resolved_path}")
        
        self.client = chromadb.PersistentClient(path=resolved_path)
        self.collection = self.client.get_collection(name=collection_name)

    def query_vectors(
        self,
        query_texts: List[str],
        n_results: int,
        where_clause: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where_clause
        )

    def count(self) -> int:
        return self.collection.count()
