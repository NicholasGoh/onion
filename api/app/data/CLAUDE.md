# Data Layer

## Entities

Plain dataclasses with no dependencies. Two per domain: `Thing` (with id) and `ThingData` (creation input, no id).

```python
@dataclass
class Thing:
    id: int
    name: str

@dataclass
class ThingData:
    name: str
```

## Interfaces

One generic ABC: `IRepository[T, TCreate]` with `create`, `get_by_id`, `get_all`, `delete`. Don't add pagination, search, or filtering here — those belong in the service layer.

## Repositories

Implement `IRepository` with SQLModel. Each repository has a companion `ThingModel(SQLModel, table=True)` with `to_entity()` for converting DB rows to domain dataclasses.

```python
class ThingRepository(IRepository[Thing, ThingData]):
    def __init__(self, session: Session):
        self.session = session
    ...
```

Repositories are minimal — no business logic, no query filtering beyond primary key lookups.

## infra/

Reserved for external service clients (LLM, Gitea, Langfuse). Define the interface in `interfaces.py`, implement in `infra/<client>.py`. Don't create `infra/` until you need it.
