```
app/
├── __init__.py
│
├── routers/                # Layer 1: Presentation
│   ├── __init__.py         #   ↓
│   └── items.py            #   ├─→ api_contracts
│                           #   └─→ orchestration
│
├── api_contracts/          # Layer 2: DTOs
│   ├── __init__.py         #   ↓
│   └── item.py             #   └─→ entities
│                           #
├── orchestration/          # Layer 3: Workflow coordination
│   ├── __init__.py         #   ↓
│   └── item_service.py     #   ├─→ business
│                           #   └─→ entities
│
├── business/               # Layer 4: DDD Rules and Validations
│   ├── __init__.py         #   ↓
│   └── item_domain.py      #   └─→ entities
│                           #
├── entities/               # Layer 5: Domain Models + Interfaces
│   ├── __init__.py         #   ↑
│   ├── item.py             #   ↑
│   └── interfaces.py       #   ↑
│                           #   ↑
└── database/               # Layer 6: ORM
    ├── __init__.py         #   └─→ entities (implements interfaces)
    └── item.py
```
