import json
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import settings
from app.repositories.base import BaseTraceRepository
from app.repositories.db_schema import Base

class TraceRunModel(Base):
    __tablename__ = "trace_runs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(100), unique=True, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    payload_json = Column(Text, nullable=False)

class PostgresTraceRepository(BaseTraceRepository):
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

    def _get_session(self) -> Session:
        if self._external_session:
            return self._external_session
        return self.session_factory()

    def get_history(self, run_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        session = self._get_session()
        try:
            query = session.query(TraceRunModel)
            if run_id:
                query = query.filter(TraceRunModel.run_id == run_id)
            query = query.order_by(TraceRunModel.timestamp.desc())
            if limit:
                query = query.limit(limit)

            runs = query.all()
            return [json.loads(r.payload_json) for r in runs]
        finally:
            if not self._external_session:
                session.close()

    def save_run(self, run_result: Dict[str, Any]) -> bool:
        session = self._get_session()
        try:
            rid = run_result.get("run_id", "unknown_run")
            existing = session.query(TraceRunModel).filter(TraceRunModel.run_id == rid).first()
            if not existing:
                existing = TraceRunModel(run_id=rid)
                session.add(existing)

            existing.payload_json = json.dumps(run_result)
            if not self._external_session:
                session.commit()
            return True
        except Exception:
            if not self._external_session:
                session.rollback()
            return False
        finally:
            if not self._external_session:
                session.close()
