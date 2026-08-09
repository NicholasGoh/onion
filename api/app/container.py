from dependency_injector import containers, providers

from app.data.config import get_session
from app.data.infra.order_repository import OrderRepository
from app.data.infra.repositories import ItemRepository
from app.service.item_service import ItemService
from app.service.order_service import OrderService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=["app.api.routes", "app.api.order_routes"]
    )

    db_session = providers.Resource(get_session)

    item_repository = providers.Factory(ItemRepository, session=db_session)
    order_repository = providers.Factory(OrderRepository, session=db_session)

    item_service = providers.Factory(ItemService, repository=item_repository)
    order_service = providers.Factory(
        OrderService,
        repository=order_repository,
        item_service=item_service,
    )
