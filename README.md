# Flow Manager (FastAPI + PostgreSQL + Alembic)

A simple **Flow Manager** microservice built with **FastAPI** where tasks are executed **sequentially** and controlled by **conditions**.  
The flow definitions are stored in PostgreSQL, and schema changes are managed using **Alembic** migrations.

---

## 🔧 Tech Stack

- Python 3.9+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic / pydantic-settings
- Uvicorn

---

## 📁 Project Structure

```bash
flow_manager/
│
├── alembic/
│   ├── env.py
│   └── versions/           # auto-generated migration files go here
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── flow_routes.py  # /flow/run endpoint
│   │
│   ├── core/
│   │   ├── settings.py     # reads .env (POSTGRES_* vars)
│   │   ├── config.py       # builds DATABASE_URL
│   │   └── logger.py       # app logger
│   │
│   ├── db/
│   │   ├── database.py     # SQLAlchemy engine & SessionLocal
│   │   ├── models.py       # FlowDefinition, FlowRun, TaskRun models
│   │   └── repositories.py # CRUD helpers for flows and runs
│   │
│   ├── flows/
│   │   ├── engine.py       # run_flow() – core flow execution logic
│   │   ├── task_result.py  # TaskResult dataclass
│   │   ├── task_registry.py# maps task names → functions
│   │   └── tasks/
│   │       ├── task1_fetch.py
│   │       ├── task2_process.py
│   │       └── task3_store.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   └── flow_schema.py  # FlowRequest, FlowDefinitionSchema
│   │
│   └── __init__.py
│
├── alembic.ini
├── requirements.txt
└── .env
```

## 1. Prerequisites

```bash
Python 3.9+
PostgreSQL installed and running locally
```


## 2. Clone the Repository
```bash
git clone <your-repo-url> flow_manager
cd flow_manager
```


## 3. Create & Activate Virtualenv
```bash
python3.9 -m venv venv
source venv/bin/activate   # on macOS/Linux
# venv\Scripts\activate    # on Windows
```


## 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Make sure you have psycopg2 installed (usually via psycopg2-binary in requirements.txt).

## 5. Configure Environment Variables (.env)

```bash
Create a .env file in the project root:

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=flow_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

These values must match your local PostgreSQL setup.

## 6. Create PostgreSQL Database

```bash
Log into PostgreSQL and create the database:
psql -U postgres

Inside psql:
CREATE DATABASE flow_db;
\q

Or in one line (mac/Linux):
createdb -U postgres flow_db
```

## 7. Alembic Setup & Migrations

```bash
7.1 Ensure alembic/env.py is wired to your app
Your alembic/env.py should:

Import Base from app.db.models
Import config from app.core.config

Use config.DATABASE_URL as the DB URL
Set target_metadata = Base.metadata
```

## 7.2 Generate Initial Migration (only first time)

```bash
If you haven’t created any migration yet:

alembic revision --autogenerate -m "initial tables"


This will create a file under alembic/versions/ with the SQL for your tables.

Review it if you want, then apply it:

alembic upgrade head

Later, when you change models again:

alembic revision --autogenerate -m "some change"
alembic upgrade head
```

## 8. Run the FastAPI App

```bash
From the project root:
uvicorn app.main:app --reload

You should see something like:
Uvicorn running on http://127.0.0.1:8000

Open:
Docs: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc
```

## 9. API – Run a Flow
```bash
Endpoint
POST /flow/run
Content-Type: application/json

Sample Request Body
{
  "flow": {
    "id": "flow123",
    "name": "Data processing flow",
    "start_task": "task1",
    "tasks": [
      {
        "name": "task1",
        "description": "Fetch data"
      },
      {
        "name": "task2",
        "description": "Process data"
      },
      {
        "name": "task3",
        "description": "Store data"
      }
    ],
    "conditions": [
      {
        "name": "condition_task1_result",
        "description": "Evaluate result of task1",
        "source_task": "task1",
        "outcome": "success",
        "target_task_success": "task2",
        "target_task_failure": "end"
      },
      {
        "name": "condition_task2_result",
        "description": "Evaluate result of task2",
        "source_task": "task2",
        "outcome": "success",
        "target_task_success": "task3",
        "target_task_failure": "end"
      }
    ]
  }
}

Sample Response (happy path)
{
  "flow_run_id": 1,
  "executed_tasks": ["task1", "task2", "task3"],
  "final_output": {
    "stored": true
  }
}
```


