from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.api.crud_router import add_get_by_id, make_crud_router
from app.api.items.contracts import ItemCreate, ItemRead
from app.container import Container
from app.service.item_service import ItemService

router = make_crud_router(
    prefix="/items",
    tag="items",
    create_dto=ItemCreate,
    read_dto=ItemRead,
    service_provider=Provide[Container.item_service],
)


@router.get("/search", response_model=list[ItemRead])
@inject
def search_items(
    q: str,
    service: ItemService = Depends(Provide[Container.item_service]),
):
    domain_items = service.search(q)
    return [ItemRead.from_entity(item) for item in domain_items]


add_get_by_id(
    router,
    tag="items",
    read_dto=ItemRead,
    service_provider=Provide[Container.item_service],
)
