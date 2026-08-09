# Testing

Every line in this repo is liability — including tests. A test should only exist if it guards a decision made in this codebase.

Before writing a test, ask: if this fails, is the fix in our code or in a `pip install` / `npm install`? If the fix is an upgrade, don't write the test.

## Do not test

- **Enum member values.** The definition is the assertion. Don't assert `Status.ACTIVE.value == "active"`.
- **Vendor library behavior.** Don't test that Pydantic rejects `None`, that SQLModel round-trips a row, or that FastAPI returns 422 on bad input.
- **Type system guarantees.** Don't assert a dataclass has fields or that an ABC raises `NotImplementedError`. Run type checkers in CI instead.
- **Generated schema snapshots.** Don't snapshot OpenAPI output or migration SQL — these break on every library patch with zero signal.

## Do test

- Validation rules we defined (empty name rejection, character limits)
- Mapping logic between layers (entity ↔ model ↔ contract conversions)
- Business workflows that coordinate multiple steps
- Edge cases in search, filtering, or transformation logic
- Integration tests that wiring works end-to-end (POST creates a retrievable item)
- Error handling paths we chose (404 on missing, 400 on invalid)
