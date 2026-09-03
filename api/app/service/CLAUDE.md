# Service Layer

## CrudService

`CrudService[T, TCreate]` wraps an `IRepository[T, TCreate]` and exposes the four CRUD operations (`create`, `get`, `get_all`, `delete`) by delegating straight to the repository. It carries no business logic of its own - it exists so pure-CRUD domains don't need a bespoke service class, and so services with real logic have a base to extend.

## When to create a service

| Scenario | What to use |
|----------|-------------|
| Pure CRUD | `CrudService[T, TCreate]` directly in container |
| CRUD + validation or extra methods | Extend `CrudService` |
| Cross-entity orchestration | Extend `CrudService`, inject other services |

Don't create a service class just for uniformity. If there's no business logic, register `CrudService` directly:

```python
# container.py — no TagService needed
tag_service = providers.Factory(CrudService, repository=tag_repository)
```

## Extending CrudService

Override `create` for validation. Add methods for domain-specific operations. Call `super()` for the CRUD parts.

```python
class ItemService(CrudService[Item, ItemData]):
    def create(self, data: ItemData) -> Item:
        self._validate(data)       # your decision
        return super().create(data) # delegate CRUD
    
    def search(self, query: str) -> list[Item]:
        ...                         # your logic
```

## Service-to-service coupling

Services may depend on other services. Wire through DI, never instantiate directly.

```python
class OrderService(CrudService[Order, OrderData]):
    def __init__(self, repository, item_service: ItemService):
        super().__init__(repository)
        self._item_service = item_service
```

Keep coupling unidirectional. If two services need each other, extract shared logic into a third.
