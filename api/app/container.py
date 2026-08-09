from dependency_injector import containers, providers

from app.data.config import get_session
from app.data.infra.repositories import ItemRepository
from app.service.item_service import ItemService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["app.api.routes"])

    db_session = providers.Resource(get_session)

    item_repository = providers.Factory(ItemRepository, session=db_session)

    item_service = providers.Factory(
        ItemService, repository=item_repository
    )
