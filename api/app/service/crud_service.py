from typing import Generic, TypeVar

from app.data.interfaces import IRepository

T = TypeVar("T")
TCreate = TypeVar("TCreate")


class CrudService(Generic[T, TCreate]):

    def __init__(self, repository: IRepository[T, TCreate]):
        self._repository = repository

    def create(self, data: TCreate) -> T:
        return self._repository.create(data)

    def get(self, id: int) -> T | None:
        return self._repository.get_by_id(id)

    def get_all(self) -> list[T]:
        return self._repository.get_all()

    def delete(self, id: int) -> bool:
        return self._repository.delete(id)
