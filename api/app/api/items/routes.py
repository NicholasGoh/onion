from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.api.items.contracts import ItemCreate, ItemRead
from app.container import Container
from app.service.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemRead)
@inject
def create_item(
    item: ItemCreate,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    try:
        domain_item = service.create(item.to_entity())
        return ItemRead.from_entity(domain_item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ItemRead])
@inject
def get_items(
    service: ItemService = Depends(Provide[Container.item_service]),
):
    domain_items = service.get_all()
    return [ItemRead.from_entity(item) for item in domain_items]


@router.get("/search", response_model=list[ItemRead])
@inject
def search_items(
    q: str,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    domain_items = service.search(q)
    return [ItemRead.from_entity(item) for item in domain_items]


@router.get("/{item_id}", response_model=ItemRead)
@inject
def get_item(
    item_id: int,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    domain_item = service.get(item_id)
    if not domain_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemRead.from_entity(domain_item)
