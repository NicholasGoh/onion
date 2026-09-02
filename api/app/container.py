from dependency_injector import containers, providers

from app.data.config import get_engine, get_session
from app.data.item_repository import ItemRepository
from app.data.order_repository import OrderRepository
from app.data.tag_repository import TagRepository
from app.service.crud_service import CrudService
from app.service.item_service import ItemService
from app.service.order_service import OrderService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=["app.api.items.routes", "app.api.orders.routes", "app.api.tags.routes"]
    )

    db_engine = providers.Resource(get_engine)
    db_session = providers.Resource(get_session, engine=db_engine)

    item_repository = providers.Factory(ItemRepository, session=db_session)
    order_repository = providers.Factory(OrderRepository, session=db_session)
    tag_repository = providers.Factory(TagRepository, session=db_session)

    item_service = providers.Factory(ItemService, repository=item_repository)
    order_service = providers.Factory(
        OrderService,
        repository=order_repository,
        item_service=item_service,
    )
    tag_service = providers.Factory(CrudService, repository=tag_repository)
