from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.api_contracts.item import ItemCreate, ItemRead
from app.container import Container
from app.orchestration.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemRead)
@inject
def create_item(
    item: ItemCreate,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    try:
        domain_item = service.create_item(item.to_entities())
        return ItemRead.from_entities(domain_item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{item_id}", response_model=ItemRead)
@inject
def get_item(
    item_id: int,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    domain_item = service.get_item(item_id)
    if not domain_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemRead.from_entities(domain_item)


@router.get("/", response_model=list[ItemRead])
@inject
def get_items(
    service: ItemService = Depends(Provide[Container.item_service]),
):
    domain_items = service.get_items()
    return [ItemRead.from_entities(item) for item in domain_items]


@router.get("/search", response_model=list[ItemRead])
@inject
def search_items(
    q: str,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    """Search items by name or description"""
    domain_items = service.search_items(q)
    return [ItemRead.from_entities(item) for item in domain_items]
