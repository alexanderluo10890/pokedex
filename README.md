# 🐱‍👤 Pokedex API

A simple **RESTful API** built with **FastAPI** that allows you to create, read, and update Pokémon data. The project uses **Pydantic** for data validation and a **JSON file** as lightweight storage, making it perfect for learning how FastAPI works under the hood.

---

## 🚀 Features

* 🔍 Fetch Pokémon by ID
* ➕ Add new Pokémon
* ✏️ Update existing Pokémon (partial updates)
* ✅ Automatic request validation with Pydantic
* 🧵 Thread-safe file writes using locks
* 📄 JSON-based persistence (no database required)

---

## 🛠 Tech Stack

* **Python 3.9+**
* **FastAPI** – API framework
* **Pydantic** – data validation & parsing
* **Uvicorn** – ASGI server
* **JSON** – data storage

---

## 📂 Project Structure

```
.
├── main.py          # FastAPI application
├── pokedex.json    # Pokémon data storage
├── README.md       # Project documentation
```

---

## ▶️ Getting Started

### 1️⃣ Install dependencies

```bash
pip install fastapi uvicorn
```

### 2️⃣ Run the server

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📘 API Endpoints

### 🔹 Root

```http
GET /
```

Returns a welcome message.

---

### 🔹 Get Pokémon by ID

```http
GET /pokemon/{id}
```

Example:

```bash
curl http://127.0.0.1:8000/pokemon/6
```

---

### 🔹 Add a Pokémon

```http
POST /pokemon
```

Request body:

```json
{
  "id": 6,
  "name": "Charizard",
  "type": ["Fire", "Flying"]
}
```

* Returns **201 Created** on success
* Rejects duplicate IDs automatically

---

### 🔹 Update a Pokémon

```http
PATCH /pokemon/{id}
```

Request body (partial update supported):

```json
{
  "name": "Mega Charizard X"
}
```

---

## 🧠 How It Works

* **FastAPI** inspects function signatures and type hints
* **Pydantic models** validate and parse incoming JSON
* Path parameters come from the URL (e.g. `/pokemon/6`)
* Request bodies are converted into Python objects
* Data is stored in memory and synced to `pokedex.json`

---

## ⚠️ Notes & Limitations

* JSON file storage is not ideal for large-scale apps
* Data resets if the file is deleted or corrupted
* Intended for learning & small projects

---

## ✨ Why This Project

This project is designed to:

* Learn **FastAPI request lifecycle**
* Understand **Pydantic validation**
* Practice building clean REST APIs

---

## 📜 License

MIT License – feel free to use and modify.

---

How to run file locally: uv run uvicorn main:app --reload
go to local host then add /docs to test the api

Happy hacking! 🚀
