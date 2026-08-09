# Presentation Layer

Routes and contracts grouped by domain (`items/`, `orders/`, etc.).

## Adding a new domain

Create `<domain>/routes.py` and `<domain>/contracts.py`. Register the router in `main.py` and add the wiring module to `container.py`.

## Contracts

Contracts convert between HTTP and domain. `to_entity()` on request DTOs, `from_entity()` on response DTOs. Never pass Pydantic models into the service layer.

```python
class ThingCreate(BaseModel):
    name: str
    def to_entity(self) -> ThingData:
        return ThingData(name=self.name)

class ThingRead(BaseModel):
    id: int
    name: str
    @classmethod
    def from_entity(cls, thing: Thing) -> "ThingRead":
        return cls(id=thing.id, name=thing.name)
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
