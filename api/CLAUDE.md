# API

Python 3.13+ / FastAPI / SQLModel / dependency-injector / PostgreSQL.

## Architecture — 3 layers

```
app/
├── __init__.py
│
├── api/                        # Layer 1: Presentation
│   ├── __init__.py
│   ├── routes.py               #   Item routes
│   ├── contracts.py            #   Item request/response DTOs
│   ├── order_routes.py         #   Order routes
│   └── order_contracts.py      #   Order request/response DTOs
│
├── service/                    # Layer 2: Business Logic
│   ├── __init__.py
│   ├── crud_service.py         #   Generic CRUD (wraps IRepository)
│   ├── item_service.py         #   Extends CrudService, adds validation + search
│   └── order_service.py        #   Extends CrudService, couples with ItemService
│
├── data/                       # Layer 3: Data Access
│   ├── __init__.py
│   ├── entities.py             #   Domain dataclasses (no deps)
│   ├── interfaces.py           #   Generic IRepository ABC
│   ├── config.py               #   DB engine + session
│   └── infra/                  #   External implementations
│       ├── __init__.py
│       ├── repositories.py     #   Item SQLModel repository
│       └── order_repository.py #   Order SQLModel repository
│
├── container.py                # DI wiring
└── main.py                     # FastAPI entry point
```

Dependencies flow inward: `api → service → data`. Never import from an outer layer.

Services may depend on other services for cross-entity orchestration (e.g. OrderService → ItemService to validate item existence). These couplings are wired through DI, never direct instantiation.
