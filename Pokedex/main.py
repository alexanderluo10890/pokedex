from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import logging
import threading

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Thread lock for concurrency safety
lock = threading.Lock()

# Function to load Pokémon data from JSON file
def load_pokemon_data() -> List[dict]:
    # if not os.path.exists("pokedex.json"):
    #     # Create an empty JSON file if it doesn't exist
    #     with open("pokedex.json", "w") as file:
    #         json.dump([], file)
    try:
        with open("pokedex.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from 'pokedex.json'")
        return []

# Function to save Pokémon data to JSON file
def save_pokemon_data(data: List[dict]):
    try:
        with lock:  # Ensure thread safety
            with open("pokedex.json", "w") as file:
                json_data = {"pokemon": data}
                json.dump(json_data, file, indent=4)
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")

# Load Pokémon data at startup
pokemon_list = load_pokemon_data()['pokemon'] # type: ignore

# Models
class Pokemon(BaseModel):
    id: int
    name: str
    type: List[str]

class UpdatePokemon(BaseModel):
    name: Optional[str] = None
    type: Optional[List[str]] = None

# Exception handler for unexpected errors
@app.exception_handler(Exception)
async def handle_all_exceptions(request, exc):
    logging.error(f"Unhandled exception: {exc}")
    return {"detail": "Internal Server Error"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Pokedex API"}

# Fetch Pokémon by ID
@app.get("/pokemon/{id}")
def get_pokemon(id: int):
    # print(pokemon_list)
    for pokemon in pokemon_list: # type: ignore
        if pokemon['id'] == id:
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

# Add a new Pokémon
@app.post("/pokemon", status_code=201)
def add_pokemon(pokemon: Pokemon):
    for p in pokemon_list:
      if p["id"] == pokemon.id: # type: ignore
        raise HTTPException(status_code=400, detail="Pokemon with this ID already exists")
    
    pokemon_list.append(pokemon.dict()) # type: ignore

    pokemon_list.sort(key=lambda x: x["id"]) #lambda function

    save_pokemon_data(pokemon_list)
    return pokemon_list

# Update a Pokémon
@app.patch("/pokemon/{id}")
def update_pokemon(id: int, updates: UpdatePokemon):
    for pokemon in pokemon_list: # type: ignore
        if pokemon["id"] == id:
            if updates.name:
                pokemon["name"] = updates.name
            if updates.type:
                pokemon["type"] = updates.type
            
            save_pokemon_data(pokemon_list)
            return {"message": "Pokemon updated successfully", "pokemon": pokemon}
    
    raise HTTPException(status_code=404, detail="Pokemon not found")
