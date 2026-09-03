from dependency_injector.wiring import Provide

from app.api.crud_router import add_get_by_id, make_crud_router
from app.api.orders.contracts import OrderCreate, OrderRead
from app.container import Container

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
