# API

Python 3.13+ / FastAPI / SQLModel / dependency-injector / PostgreSQL.

## Architecture — 3 layers

```
app/
├── api/            # Layer 1: Presentation (routes + request/response contracts)
├── service/        # Layer 2: Business logic (validation + orchestration)
└── data/           # Layer 3: Data access (entities, interfaces, repositories, DB config)
```

Dependencies flow inward: `api → service → data`. Never import from an outer layer.

## Testing guidance

Inherits root CLAUDE.md rules. API-specific examples:

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
