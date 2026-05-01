# Pokedex API

A **RESTful API** built with **FastAPI** that lets you create, read, and update Pokémon data. Uses **Pydantic** for validation and a **JSON file** as lightweight storage — built to learn how FastAPI works under the hood.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- Fetch Pokémon by ID
- Add new Pokémon with automatic duplicate rejection
- Partial updates via PATCH (name, type, or both)
- Automatic request validation with Pydantic
- Thread-safe file writes using locks
- JSON-based persistence — no database required

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Language |
| FastAPI | API framework |
| Pydantic | Data validation & parsing |
| Uvicorn | ASGI server |
| pytest | Testing |
| JSON | Data storage |

---

## Project Structure

```
.
├── main.py          # FastAPI app & endpoints
├── test_main.py     # pytest test suite
├── pokedex.json     # Pokémon data storage
└── README.md
```

---

## Getting Started

### Install dependencies

```bash
pip install fastapi uvicorn
```

### Run the server

```bash
uvicorn main:app --reload
```

Or with `uv`:

```bash
uv run uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000` — visit `/docs` for the interactive Swagger UI.

---

## API Endpoints

### GET /
Returns a welcome message.

### GET /pokemon/{id}
Fetch a Pokémon by ID.

```bash
curl http://127.0.0.1:8000/pokemon/6
```

### POST /pokemon
Add a new Pokémon. Returns 201 on success, 400 if the ID already exists.

```json
{
  "id": 6,
  "name": "Charizard",
  "type": ["Fire", "Flying"]
}
```

### PATCH /pokemon/{id}
Partial update — send only the fields you want to change.

```json
{
  "name": "Mega Charizard X"
}
```

---

## Testing

```bash
pytest test_main.py
```

Tests cover all endpoints, validation errors, duplicate ID rejection, sort order after inserts, and data persistence helpers.

---

## How It Works

- FastAPI inspects function signatures and type hints to build routes automatically
- Pydantic models validate and parse incoming JSON before it hits your handler
- A threading lock wraps all file writes to prevent race conditions
- The in-memory list stays sorted by ID after every insert

---

## What I Learned

- How FastAPI uses type hints to handle routing, validation, and docs generation with minimal boilerplate
- How Pydantic models enforce schema at the boundary so the rest of the code can trust the data
- Why thread locks matter even in small projects — file writes are not atomic
- How to structure pytest fixtures for setup/teardown without leaking test data

---

## Potential Improvements

- Swap JSON storage for SQLite or PostgreSQL for real persistence
- Add a `GET /pokemon` endpoint to list all Pokémon with pagination
- Add `DELETE /pokemon/{id}`
- Dockerize the app for easier deployment

---

## License

MIT — feel free to use and modify.
