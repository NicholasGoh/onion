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
