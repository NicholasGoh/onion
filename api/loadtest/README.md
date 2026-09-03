# k6 load test

Covers items, tags, and orders CRUD plus item search and order quoting.

## Run

```bash
# api must be running (e.g. `docker compose up api postgres`)
k6 run api/loadtest/k6.js
```

## Options

- `BASE_URL` - target host (default `http://localhost:8000`)
- `SESSION_TOKEN` - Kratos session token, sent as `X-Session-Token` on every request (all routes require authn at the router level). If unset, every request is expected to 401.

```bash
BASE_URL=http://localhost:8000 SESSION_TOKEN=<token> k6 run api/loadtest/k6.js
```
