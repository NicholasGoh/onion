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
│   ├── interfaces.py       #   Repository ABCs (→ entities)
│   ├── repositories.py     #   SQLModel implementation (→ interfaces, entities)
│   └── config.py           #   DB engine + session
│
├── container.py            # DI wiring
└── main.py                 # FastAPI entry point
```
