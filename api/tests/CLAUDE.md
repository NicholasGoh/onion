# API Tests

Every line in this repo is liability — including tests. A test should only exist if it guards a decision made in this codebase.

Before writing a test, ask: if this fails, is the fix in our code or in a `pip install` / `npm install`? If the fix is an upgrade, don't write the test.

## Do not test

- **Enum member values.** The definition is the assertion. Don't assert `Status.ACTIVE.value == "active"`.
- **Vendor library behavior.** Don't test that Pydantic rejects `None`, that SQLModel round-trips a row, or that FastAPI returns 422 on bad input.
- **Type system guarantees.** Don't assert a dataclass has fields or that an ABC raises `NotImplementedError`. Run type checkers in CI instead.
- **Generated schema snapshots.** Don't snapshot OpenAPI output or migration SQL — these break on every library patch with zero signal.
- **DI provider construction.** Don't assert `isinstance(container.service(), MyService)` — that tests `providers.Factory` calling a constructor, which is the DI framework's job, not ours.

## Do test

- Validation rules we defined (empty name rejection, character limits)
- Mapping logic between layers (entity ↔ model ↔ contract conversions)
- Business workflows that coordinate multiple steps
- Edge cases in search, filtering, or transformation logic
- Integration tests that wiring works end-to-end (POST creates a retrievable item)
- Error handling paths we chose (404 on missing, 400 on invalid)
- **DI wiring** — that a route's `Provide[Container.x]` resolves to the provider we intended. Override the provider with a `MagicMock`, hit the route via `TestClient`, assert the mock was called. This catches a typo'd or swapped provider reference that a same-shaped real service would silently pass.

Test the service layer for validation, search, and orchestration logic. Test the data layer only when a repository contains custom query logic. Test the api layer for contract serialization and error codes. Don't test inside a layer to verify the framework still works.

## Examples

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

**Wasteful** — retests provider construction:
```python
def test_container_resolves_service():
    service = container.item_service()
    assert isinstance(service, ItemService)
```

**Worth it** — integration test that wiring works:
```python
def test_create_and_get_item(client):
    resp = client.post("/items/", json={"name": "Widget"})
    item_id = resp.json()["id"]
    resp = client.get(f"/items/{item_id}")
    assert resp.json()["name"] == "Widget"
```

**Worth it** — proves a route resolves to the intended provider:
```python
def test_items_route_wired_to_item_service():
    mock_service = MagicMock(get_all=MagicMock(return_value=[]))
    with container.item_service.override(mock_service):
        with TestClient(app) as client:
            client.get("/items/")
    mock_service.get_all.assert_called_once()
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
