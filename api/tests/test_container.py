from app.container import Container
from app.data.item_repository import ItemRepository
from app.service.item_service import ItemService


def test_container_resolves_item_service():
    container = Container()
    container.init_resources()
    service = container.item_service()
    assert isinstance(service, ItemService)


def test_container_resolves_item_repository():
    container = Container()
    container.init_resources()
    repo = container.item_repository()
    assert isinstance(repo, ItemRepository)


def test_item_service_receives_repository():
    container = Container()
    container.init_resources()
    service = container.item_service()
    assert isinstance(service._repository, ItemRepository)
