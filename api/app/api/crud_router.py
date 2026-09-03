from typing import Protocol, TypeVar

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, HTTPException

from app.service.crud_service import CrudService

T = TypeVar("T")
TCreate = TypeVar("TCreate")


class CreateDto(Protocol[TCreate]):
    def to_entity(self) -> TCreate: ...


class ReadDto(Protocol[T]):
    @classmethod
    def from_entity(cls, entity: T) -> "ReadDto[T]": ...


def make_crud_router(
    *,
    prefix: str,
    tag: str,
    create_dto: type[CreateDto[TCreate]],
    read_dto: type[ReadDto[T]],
    service_provider,
) -> APIRouter:
    """Builds a router with create/list routes wired. Call `add_get_by_id`
    after registering any custom static-path routes (e.g. "/search"), since
    "/{id}" would otherwise shadow them."""
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.post("/", response_model=read_dto)
    @inject
    def create(data: create_dto, service: CrudService[T, TCreate] = Depends(service_provider)):
        try:
            entity = service.create(data.to_entity())
            return read_dto.from_entity(entity)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/", response_model=list[read_dto])
    @inject
    def get_all(service: CrudService[T, TCreate] = Depends(service_provider)):
        entities = service.get_all()
        return [read_dto.from_entity(entity) for entity in entities]

    return router


def add_get_by_id(
    router: APIRouter,
    *,
    tag: str,
    read_dto: type[ReadDto[T]],
    service_provider,
) -> None:
    @router.get("/{id}", response_model=read_dto)
    @inject
    def get(id: int, service: CrudService = Depends(service_provider)):
        entity = service.get(id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"{tag[:-1].capitalize()} not found")
        return read_dto.from_entity(entity)
