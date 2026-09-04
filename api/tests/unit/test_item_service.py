import pytest

from app.data.entities import ItemData
from app.service.item_service import ItemService
from tests.conftest import FakeItemRepository


def test_create_item_rejects_empty_name(item_repo):
    service = ItemService(repository=item_repo)
    with pytest.raises(ValueError, match="cannot be empty"):
        service.create(ItemData(name=""))


def test_create_item_rejects_whitespace_name(item_repo):
    service = ItemService(repository=item_repo)
    with pytest.raises(ValueError, match="cannot be empty"):
        service.create(ItemData(name="   "))


def test_create_item_rejects_long_name(item_repo):
    service = ItemService(repository=item_repo)
    with pytest.raises(ValueError, match="100 characters"):
        service.create(ItemData(name="x" * 101))


def test_create_item_rejects_long_description(item_repo):
    service = ItemService(repository=item_repo)
    with pytest.raises(ValueError, match="500 characters"):
        service.create(ItemData(name="valid", description="x" * 501))


def test_create_item_succeeds(item_repo):
    service = ItemService(repository=item_repo)
    item = service.create(ItemData(name="Widget", description="A widget"))
    assert item.name == "Widget"
    assert item.id == 1


def test_search_filters_by_name(item_repo_with_data):
    service = ItemService(repository=item_repo_with_data)
    results = service.search("bluetooth")
    assert len(results) == 1
    assert results[0].name == "Bluetooth Speaker"


def test_search_matches_description(item_repo_with_data):
    service = ItemService(repository=item_repo_with_data)
    results = service.search("charging")
    assert len(results) == 1
    assert results[0].name == "USB Cable"


def test_search_case_insensitive(item_repo_with_data):
    service = ItemService(repository=item_repo_with_data)
    results = service.search("BLUE")
    assert len(results) == 2


def test_search_empty_query_returns_all(item_repo_with_data):
    service = ItemService(repository=item_repo_with_data)
    results = service.search("  ")
    assert len(results) == 3
