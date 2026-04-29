# Task Context — backend-implementation

## Task Description
Implement backend for internal task management system according to the technical specification (ТЗ.md) and implementation plan (BACKEND_PLAN.md).

## Requirements
- Backend API for managing InternalTask entities
- Clean Architecture (3-layer: Core, Application, Infrastructure)
- SQLite database with SQLAlchemy (async)
- FastAPI REST API
- Full test coverage (pytest)
- Logging with Loguru
- Monitoring description (Grafana, Sentry)

## Technical Details

### Domain Model
- **Entity**: InternalTask
- **Fields**: id, booking_id, title, status, created_at
- **Status Enum**: OPEN, IN_PROGRESS, CLOSED

### API Endpoints
- `POST /bookings/{booking_id}/tasks` - Create task
- `GET /bookings/{booking_id}/tasks` - Get tasks by booking
- `PATCH /tasks/{task_id}/status` - Update task status

### Business Rules
- No duplicate tasks (same booking_id + title)
- Status transitions must be valid
- All operations must be logged

### Architecture Constraints
- Core layer must have no external dependencies
- Use dependency injection for all components
- Follow SOLID principles
- All code in English, type hints required

## Acceptance Criteria
- All endpoints implemented and working
- Tests pass (100% coverage for critical paths)
- Clean code standards met
- Documentation in README.md
- execution_log.md updated