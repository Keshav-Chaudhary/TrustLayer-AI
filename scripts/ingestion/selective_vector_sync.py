import os
import sys
import hashlib
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.config import settings
from app.repositories.db_schema import EmbeddingDocumentModel

def sync_selective_vectors(
    affected_hotel_ids: List[str],
    mode: str = "dry-run",
    db_url: Optional[str] = None
) -> Dict[str, Any]:
    target_db_url = db_url or settings.DATABASE_URL
    assert target_db_url and "postgresql" in target_db_url, "DATABASE_URL must be configured for PostgreSQL"

    engine = create_engine(target_db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        if not affected_hotel_ids:
            return {"status": "NO_OP", "affected_hotels": 0, "chunks_regenerated": 0}

        # Query existing vector chunks for affected hotel IDs
        chunks_to_update = session.query(EmbeddingDocumentModel).filter(EmbeddingDocumentModel.hotel_id.in_(affected_hotel_ids)).all()

        if mode == "dry-run":
            return {
                "status": "DRY_RUN",
                "affected_hotels": len(affected_hotel_ids),
                "chunks_to_regenerate": len(chunks_to_update)
            }

        if not chunks_to_update:
            return {"status": "SUCCESS", "affected_hotels": len(affected_hotel_ids), "chunks_regenerated": 0}

        encoder = SentenceTransformer(settings.EMBEDDING_MODEL)

        updated_count = 0
        for chunk in chunks_to_update:
            vec = encoder.encode(chunk.snippet).tolist()
            chunk.embedding_vector = str(vec)
            updated_count += 1

        session.commit()
        return {"status": "SUCCESS", "affected_hotels": len(affected_hotel_ids), "chunks_regenerated": updated_count}
    except Exception as ex:
        session.rollback()
        raise ex
    finally:
        session.close()
