# Presentation Layer

Routes and contracts grouped by domain (`items/`, `orders/`, etc.).

## Adding a new domain

Create `<domain>/routes.py` and `<domain>/contracts.py`. Register the router in `main.py` and add the wiring module to `container.py`.

## Contracts

All contracts inherit `CamelModel` from `base.py` — serializes as camelCase for the frontend, accepts both camelCase and snake_case input. Never pass Pydantic models into the service layer.

`to_entity()` on request DTOs, `from_entity()` on response DTOs.

```python
from app.api.base import CamelModel

class ThingCreate(CamelModel):
    some_field: str  # accepts "someField" or "some_field"
    def to_entity(self) -> ThingData:
        return ThingData(some_field=self.some_field)

class ThingRead(CamelModel):
    id: int
    some_field: str  # serializes as "someField"
    @classmethod
    def from_entity(cls, thing: Thing) -> "ThingRead":
        return cls(id=thing.id, some_field=thing.some_field)
```

## Routes

Routes handle HTTP concerns only — status codes, error mapping. Business logic stays in the service layer.

```python
@router.post("/", response_model=ThingRead)
@inject
def create_thing(
    thing: ThingCreate,
    service: ThingService = Depends(Provide[Container.thing_service]),
):
    try:
        result = service.create(thing.to_entity())
        return ThingRead.from_entity(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

Map `ValueError` → 400, `None` returns → 404. Don't catch broad exceptions.
