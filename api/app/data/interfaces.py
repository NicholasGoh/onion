from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
TCreate = TypeVar("TCreate")


class IRepository(ABC, Generic[T, TCreate]):

    @abstractmethod
    def create(self, data: TCreate) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


IItemRepository = IRepository["Item", "ItemData"]


class IAuthClient(ABC):

    @abstractmethod
    def whoami(
        self, cookie: str | None = None, token: str | None = None
    ) -> "Session | None":
        """Sync session check against either a browser session cookie or an
        API client's session token - caller passes exactly one. Blocks the
        calling thread - safe from sync routes (FastAPI threadpools them),
        unsafe from async routes."""

    @abstractmethod
    async def awhoami(
        self, cookie: str | None = None, token: str | None = None
    ) -> "Session | None":
        """Async session check. Awaits without blocking the event loop."""
