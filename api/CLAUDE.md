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
