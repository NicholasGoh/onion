from dependency_injector import containers, providers

from app.business.item_domain import ItemDomain
from app.database.config import get_session
from app.database.item import ItemRepository
from app.orchestration.item_service import ItemService


class Container(containers.DeclarativeContainer):
    """DI Container for the application"""

    wiring_config = containers.WiringConfiguration(modules=["app.routers.items"])

    # Database
    db_session = providers.Resource(get_session)

    # Business
    item_domain = providers.Singleton(ItemDomain)

    # Repositories
    item_repository = providers.Factory(ItemRepository, session=db_session)

    # Services
    item_service = providers.Factory(
        ItemService, repository=item_repository, domain=item_domain
    )
