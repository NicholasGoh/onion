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

## CPU-bound methods

Decorate CPU-bound (non-I/O) service methods with `@compute` (`decorators.py`) instead of making them `async def`. It gives callers a choice of transport instead of forcing one:

- Sync route handler → call the method directly. FastAPI already runs sync routes in a threadpool, so this is fine as-is.
- Async route handler → `await method.async_(...)`. This routes the call through a threadpool so the event loop isn't blocked.

```python
class ItemService(CrudService[Item, ItemData]):
    @compute
    def score(self, item: Item) -> float:
        ...  # CPU-bound, no I/O

# sync route
service.score(item)
# async route
await service.score.async_(item)
```

Nothing enforces this at the type level - an async caller invoking `service.score(item)` directly will block the event loop instead of raising. There's no lint rule; catch it at review time. Don't reach for `@compute` on I/O-bound methods (repository calls, HTTP clients) - those should just be `async def` and awaited normally.
