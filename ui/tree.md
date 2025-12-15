```
ui/
├── pages/                    # Layer 1: Presentation (routes)
│   └── ItemsPage.tsx         #   └─→ components
│
├── components/               # Layer 2: Components + ViewModels
│   ├── ItemList.tsx          #   ├─→ queries
│   └── ItemList.vm.ts        #   ├─→ state
│                             #   └─→ entities
│
│                             # Layer 3: Orchestration
├── queries/                  #   TanStack Query (server state)
│   └── useItems.ts           #   └─→ business
│
├── store/                    #   Zustand (global UI state)
│   └── itemPreferences.ts    #
│
└── lib/
    ├── business/             # Layer 4: API ↔ Entity transform
    │   └── itemRepository.ts #   ├─→ api/contracts
    │                         #   └─→ entities
    │
    ├── entities/             # Layer 5: Domain models
    │   └── item.ts           #
    │
    └── api/                  # Layer 6: External boundary
        └── contracts/
            └── item.ts       #   DTOs (matches backend)
```
