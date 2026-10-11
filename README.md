# MyApp starter

A small, documented full-stack starting point for building an application with
Vue, Nuxt UI, FastAPI, and SQLite. It includes a telemetry dashboard with
sample metrics and a task tracker: add tasks, mark them complete, filter the
list, and remove tasks.

## Stack

- **Frontend:** Nuxt 4, Vue 3, TypeScript, and Nuxt UI.
- **Backend:** Python 3.10+, FastAPI, Pydantic, and SQLAlchemy 2.
- **Database:** SQLite, created automatically on the first API startup.
- **Tests:** pytest and FastAPI's `TestClient`.

The frontend and backend are separate applications. The browser calls the API
directly; the backend owns validation and persistence.

## Requirements

- Node.js 22.22.3+ or 24.15.0+ and npm (required by the current Nuxt release).
- Python 3.10 or newer.

## Run locally

Open two terminals from the `MyApp` directory.

### 1. Start the API

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and start the development server:

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at <http://localhost:8000>. Interactive API
documentation is at <http://localhost:8000/docs>; the health check is
<http://localhost:8000/health>.

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:3000>.

## Configuration

| Variable | Used by | Default | Purpose |
| --- | --- | --- | --- |
| `DATABASE_URL` | Backend | `sqlite:///./app.db` | SQLAlchemy database URL. The relative SQLite path is resolved from the backend working directory. |
| `FRONTEND_ORIGIN` | Backend | `http://localhost:3000` | Single browser origin allowed by CORS. |
| `NUXT_PUBLIC_API_BASE` | Frontend | `http://localhost:8000` | Base URL used by the browser to reach the API. |

For example, start the API with a different database file:

```bash
DATABASE_URL=sqlite:///./local-dev.db uvicorn app.main:app --reload
```

Set `NUXT_PUBLIC_API_BASE` at frontend build/runtime configuration time when
the API is hosted somewhere other than `http://localhost:8000`.

## API

All task endpoints are prefixed with `/api`.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check that the API is running. |
| `GET` | `/api/tasks` | List tasks; optionally use `?completed=true` or `?completed=false`. |
| `POST` | `/api/tasks` | Create a task with a `title` and optional `description`. |
| `PATCH` | `/api/tasks/{task_id}` | Set a task's `completed` state. |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task. |

Example create request:

```json
{
  "title": "Plan the next release",
  "description": "Collect the items for the first milestone."
}
```

Task titles are trimmed and must contain 1–200 characters. Descriptions can
contain up to 2,000 characters. Invalid input receives a standard FastAPI
validation response; requests for missing tasks receive `404`.

## Project layout

```text
MyApp/
├── backend/
│   ├── app/
│   │   ├── database.py     # Engine, ORM base, and request-scoped sessions
│   │   ├── main.py         # App setup, CORS, startup, and HTTP routes
│   │   ├── models.py       # SQLAlchemy database model
│   │   └── schemas.py      # Validated API request/response models
│   ├── tests/
│   │   └── test_api.py     # Isolated API integration tests
│   ├── pyproject.toml      # pytest and Ruff settings
│   └── requirements.txt
└── frontend/
    ├── app/
    │   ├── assets/css/main.css # Tailwind CSS and Nuxt UI styles
    │   ├── composables/        # Typed API client
    │   ├── pages/index.vue     # Mock telemetry dashboard
    │   ├── pages/tasks.vue     # Task-tracker screen
    │   ├── app.vue
    │   └── types/task.ts
    ├── nuxt.config.ts
    └── package.json
```

The database tables are created at API startup. SQLite's `app.db` file is
local development data and is ignored by Git. For a production application,
add schema migrations (for example, Alembic) rather than relying on
`create_all`, and use a managed database with backups.

The dashboard at `/` uses hard-coded sample telemetry for demonstration and
does not call the backend. The task tracker is available at `/tasks`. Replace
the dashboard's sample data in `frontend/app/pages/index.vue` with a typed API
client when a real telemetry source is available.

## Test and lint the backend

From `MyApp/backend` with the virtual environment active:

```bash
python -m pip install -r requirements.txt
pytest
ruff check .
```

The API tests use a temporary SQLite database; they do not depend on or modify
your development database.

## Frontend commands

From `MyApp/frontend`:

```bash
npm run dev       # Start the local development server
npm run build     # Build for production
npm run preview   # Preview the production build
npm run typecheck # Check Vue and TypeScript types
```

## Development notes

- Keep request/response validation in Pydantic schemas and persistence in
  SQLAlchemy models; add new routes to `backend/app/main.py`.
- Keep browser API calls in `frontend/app/composables/useTasksApi.ts` rather than
  embedding endpoint URLs in UI components.
- Display request failures in the interface; do not silently treat failed
  requests as successful.
- CORS is intentionally restricted to one configured development origin.
  Set `FRONTEND_ORIGIN` to the deployed frontend's exact origin in production.
- Run `npm audit` before deployment. The current upstream Nuxt dependency tree
  reports advisories; npm's suggested forced fix downgrades Nuxt to an older
  release, so it was not applied automatically.
- There is no authentication in this starter. Add authentication and
  authorization before exposing private user data.
- The UI is an example feature, not a finished product design system. Extend
  the task model and API with migrations when the domain evolves.
