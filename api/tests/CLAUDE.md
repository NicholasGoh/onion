# API Tests

Inherits `tests/CLAUDE.md`.

The API uses a 3-layer architecture (api → service → data). Each layer boundary is a place where we made a decision — a mapping, a validation rule, an error code. Tests belong at those boundaries, asserting our decisions hold. They don't belong inside a layer verifying that the framework we delegated to still works.

The service layer owns all business rules. Test validation, search, and orchestration logic there. The data layer is mostly delegation to SQLModel — only test it when a repository contains custom query logic. The api layer maps between HTTP and domain; test that our contracts serialize correctly and that our error codes match our intent.

## Wasteful vs worth it

**Wasteful** — retests SQLModel:
```python
def test_repository_creates_and_retrieves():
    repo.create(ItemData(name="x"))
    assert repo.get_by_id(1).name == "x"
```

**Worth it** — tests our search logic:
```python
def test_search_filters_by_name_substring():
    service = make_service(items=[
        ItemData(name="Bluetooth Speaker"),
        ItemData(name="USB Cable"),
    ])
    results = service.search_items("blue")
    assert len(results) == 1
```

**Wasteful** — retests Pydantic:
```python
def test_pydantic_rejects_missing_name():
    with pytest.raises(ValidationError):
        ItemCreate(name=None)
```

**Worth it** — tests our validation rule:
```python
def test_create_item_rejects_empty_name():
    service = ItemService(repository=fake_repo)
    with pytest.raises(ValueError, match="cannot be empty"):
        service.create_item(ItemData(name=""))
```

**Wasteful** — retests enum definition:
```python
def test_status_enum_values():
    assert Status.ACTIVE.value == "active"
```

**Worth it** — tests our mapping decision:
```python
def test_status_serializes_to_api_contract():
    item = Item(status=Status.ACTIVE)
    payload = ItemRead.from_entity(item)
    assert payload.status == "active"
```
