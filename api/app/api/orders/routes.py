from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.api.crud_router import add_get_by_id, make_crud_router
from app.api.orders.contracts import OrderCreate, OrderQuote, OrderRead
from app.container import Container
from app.service.order_service import OrderService

router = make_crud_router(
    prefix="/orders",
    tag="orders",
    create_dto=OrderCreate,
    read_dto=OrderRead,
    service_provider=Provide[Container.order_service],
)

add_get_by_id(
    router,
    tag="orders",
    read_dto=OrderRead,
    service_provider=Provide[Container.order_service],
)


@router.post("/quote", response_model=OrderQuote)
@inject
def quote_order(
    order: OrderCreate,
    service: OrderService = Depends(Provide[Container.order_service]),
):
    total = service.calculate_total(order.to_entity())
    return OrderQuote(total=total)
