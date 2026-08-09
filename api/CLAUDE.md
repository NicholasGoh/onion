# API

Python 3.13+ / FastAPI / SQLModel / dependency-injector / PostgreSQL.

## Architecture — 3 layers

```
app/
├── __init__.py
│
├── api/                    # Layer 1: Presentation
│   ├── __init__.py         #   ↓
│   ├── routes.py           #   ├─→ contracts
│   └── contracts.py        #   └─→ data.entities
│
├── service/                # Layer 2: Business Logic
│   ├── __init__.py         #   ↓
│   └── item_service.py     #   └─→ data (entities + interfaces)
│
├── data/                   # Layer 3: Data Access
│   ├── __init__.py         #
│   ├── entities.py         #   Domain dataclasses (no deps)
│   ├── interfaces.py       #   ABCs for all external dependencies
│   ├── config.py           #   DB engine + session
│   └── infra/              #   External implementations
│       ├── __init__.py     #
│       └── repositories.py #   SQLModel repository
│
├── container.py            # DI wiring
└── main.py                 # FastAPI entry point
```

Dependencies flow inward: `api → service → data`. Never import from an outer layer.
