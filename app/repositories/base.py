from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from app.domain.models import HotelDomainModel, ProvenanceChunk

class BaseHotelRepository(ABC):
    @abstractmethod
    def get_by_id(self, hotel_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_hotels(
        self,
        page: int = 1,
        limit: int = 20,
        area: Optional[str] = None,
        budget: Optional[str] = None,
        rating: Optional[float] = None,
        cleanliness: Optional[float] = None,
        sort_by: str = "trust_score_desc"
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_hotels(self) -> Dict[str, Dict[str, Any]]:
        pass

    @abstractmethod
    def get_area_counts(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def exists(self, hotel_id: str) -> bool:
        pass

    @abstractmethod
    def upsert(self, hotel_data: Dict[str, Any]) -> bool:
        """Future Ingestion Contract: Upsert single hotel entity"""
        pass

    @abstractmethod
    def bulk_upsert(self, hotels: List[Dict[str, Any]]) -> int:
        """Future Ingestion Contract: Bulk upsert hotel entities"""
        pass


class BaseReviewRepository(ABC):
    @abstractmethod
    def get_evidence(self, hotel_id: str) -> List[ProvenanceChunk]:
        pass

    @abstractmethod
    def get_explanation_breakdown(self, hotel_id: str) -> Dict[str, Any]:
        pass


class BaseEmbeddingRepository(ABC):
    @abstractmethod
    def query_vectors(
        self,
        query_texts: List[str],
        n_results: int,
        where_clause: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class BaseTraceRepository(ABC):
    @abstractmethod
    def get_history(self, run_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_run(self, run_result: Dict[str, Any]) -> bool:
        pass
