<div align="center">

<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png" width="120" alt="Pikachu"/>

# ⚡ Pokédex API ⚡

> *A RESTful API that lets you catch, inspect, and train Pokémon data — gotta query 'em all.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![pytest](https://img.shields.io/badge/pytest-passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

<div align="center">

## 📖 Opening the Pokédex...

<table>
<tr>
<td align="center">
<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png" width="120" alt="Bulbasaur"/><br/>
<strong>#001 Bulbasaur</strong><br/>
<code>Grass / Poison</code>
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png" width="120" alt="Charmander"/><br/>
<strong>#004 Charmander</strong><br/>
<code>Fire</code>
</td>
<td align="center">
<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/7.png" width="120" alt="Squirtle"/><br/>
<strong>#007 Squirtle</strong><br/>
<code>Water</code>
</td>
</tr>
</table>

*Choose your starter — then fetch them all via the API.*

</div>

---

## 🖥️ What Is This?

A **RESTful API** built with **FastAPI** that lets you create, read, and update Pokémon data. Uses **Pydantic** for validation and a **JSON file** as lightweight storage — built to learn how FastAPI works under the hood.

---

## ✨ Features

<table>
<tr>
<td>🔍</td><td>Fetch any Pokémon by ID</td>
</tr>
<tr>
<td>➕</td><td>Add new Pokémon with automatic duplicate rejection</td>
</tr>
<tr>
<td>✏️</td><td>Partial updates via PATCH (name, type, or both)</td>
</tr>
<tr>
<td>🛡️</td><td>Automatic request validation with Pydantic</td>
</tr>
<tr>
<td>🔒</td><td>Thread-safe file writes using locks</td>
</tr>
<tr>
<td>💾</td><td>JSON-based persistence — no database required</td>
</tr>
</table>

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Language |
| FastAPI | API framework |
| Pydantic | Data validation & parsing |
| Uvicorn | ASGI server |
| pytest | Testing |
| JSON | Data storage |

---

## 📁 Project Structure

```
pokedex/
├── main.py          # FastAPI app & endpoints
├── test_main.py     # pytest test suite
├── pokedex.json     # Pokémon data storage
└── README.md
```

---

## 🚀 Getting Started

**Install dependencies**

```bash
pip install fastapi uvicorn
```

**Run the server**

```bash
uvicorn main:app --reload
```

Or with `uv`:

```bash
uv run uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000` — visit `/docs` for the interactive Swagger UI.

---

## 🌐 API Endpoints

<div align="center">
<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png" width="160" alt="Charizard"/>

*All examples use Charizard — #006*
</div>

<br/>

### `GET /`
Returns a welcome message.

### `GET /pokemon/{id}`
Fetch a Pokémon by ID.

```bash
curl http://127.0.0.1:8000/pokemon/6
```

### `POST /pokemon`
Add a new Pokémon. Returns `201` on success, `400` if the ID already exists.

```json
{
  "id": 6,
  "name": "Charizard",
  "type": ["Fire", "Flying"]
}
```

### `PATCH /pokemon/{id}`
Partial update — send only the fields you want to change.

```json
{
  "name": "Mega Charizard X"
}
```

---

## 🧪 Testing

```bash
pytest test_main.py -v
```

Tests cover all endpoints, validation errors, duplicate ID rejection, sort order after inserts, and data persistence helpers.

---

## ⚙️ How It Works

- FastAPI inspects function signatures and type hints to build routes automatically
- Pydantic models validate and parse incoming JSON before it hits your handler
- A threading lock wraps all file writes to prevent race conditions
- The in-memory list stays sorted by ID after every insert

---

## 🧠 What I Learned

- How FastAPI uses type hints to handle routing, validation, and docs with minimal boilerplate
- How Pydantic models enforce schema at the boundary so the rest of the code can trust the data
- Why thread locks matter even in small projects — file writes are not atomic
- How to structure pytest fixtures for setup/teardown without leaking test data

---

## 🔮 Potential Improvements

- Swap JSON for SQLite or PostgreSQL for real persistence
- Add `GET /pokemon` to list all Pokémon with pagination
- Add `DELETE /pokemon/{id}`
- Dockerize the app for easier deployment

---

<div align="center">

<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png" width="100" alt="Snorlax"/>

*Pokédex closing... Snorlax used Rest.*

**MIT License** — feel free to use and modify.

</div>
