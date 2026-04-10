# SkateMap

SkateMap is a backend API for a web app that lets skateboarders discover and share street skate spots. Built with FastAPI and PostgreSQL.

---

## Features

- Browse all skate spots
- Add a spot with a name, description, and coordinates
- Upload and delete images for a spot
- Spot locations sourced from OpenStreetMap

---

## Tech Stack

- **FastAPI** — API framework with automatic OpenAPI docs
- **PostgreSQL** — primary database
- **SQLAlchemy 2.x** — ORM with typed mapped columns
- **Pydantic v2** — request/response validation and settings management
- **Uvicorn** — ASGI server
- **pytest** — test suite with a dedicated PostgreSQL test database

See [`docs/architecture.md`](docs/architecture.md) for a full breakdown of the project structure, layer diagram, request lifecycle, and data model.

---

## Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL running locally

### Install

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

Create a `.env` file at the project root. These are the defaults — adjust to match your local Postgres:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=skatemap_db
```

### Database

Create the database in Postgres:

```sql
CREATE DATABASE skatemap_db;
```

Tables are created automatically when the app starts via SQLAlchemy's `create_all`.

### Run

```bash
python run.py
```

This starts the server and opens the Swagger UI at `http://127.0.0.1:8000/docs`.

---

## Running Tests

Create a separate test database:

```sql
CREATE DATABASE skatemap_test_db;
```

Then run:

```bash
pytest
```

Tests use a dedicated PostgreSQL database. Tables are created and dropped around each test for full isolation.

---

## Docker

Build the image:

```bash
docker build -t skatemap .
```

Run the server:

```bash
docker run -p 8000:8000 skatemap
```

Run the tests inside the container:

```bash
docker run skatemap pytest
```

---

## API

Full interactive documentation is available at `/docs` once the server is running. A static OpenAPI schema is at `/openapi.json`.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/spots/` | List all spots |
| POST | `/spots/` | Create a spot |
| GET | `/spots/{id}` | Get a spot by ID |
| GET | `/spots/{id}/images` | List images for a spot |
| POST | `/spots/{id}/images` | Upload an image to a spot |
| DELETE | `/spots/{id}/images/{image_id}` | Delete an image |