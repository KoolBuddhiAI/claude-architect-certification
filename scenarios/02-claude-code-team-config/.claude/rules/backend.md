# Backend Rules (backend/)

## Code Style
- Use type hints on all function signatures
- Prefer `async def` for route handlers; use `def` only for sync utility functions
- Never use `import *`; always explicit imports

## FastAPI Patterns
- All routes return Pydantic response models — never raw dicts
- Use dependency injection for DB sessions: `db: Session = Depends(get_db)`
- Validation errors should return 422 with field-level detail, not 500

## Database
- All schema changes go through Alembic migrations — never `Base.metadata.create_all()` in production paths
- Use `with db.begin()` for transactions that modify data
- Never execute raw SQL strings; always use ORM or parameterized queries

## Testing
- Tests live in `backend/tests/` mirroring the source structure
- Use `pytest` fixtures for DB setup; never hardcode test data inline
- Every new endpoint needs at least one happy-path and one error-path test

## Security
- Never log request bodies that may contain passwords or tokens
- Validate and sanitize all user input at the route layer
- Use `secrets.token_urlsafe()` for any token generation
