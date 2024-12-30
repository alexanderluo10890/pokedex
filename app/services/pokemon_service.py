from fastapi import HTTPException
from app.utils.file_operations import load_pokemon_data, save_pokemon_data
from app.models.pokemon import Pokemon, UpdatePokemon

# Load initial data
pokemon_list = load_pokemon_data()["pokemon"]

def get_pokemon_by_id(id: int):
    """Fetch a Pokémon by its ID."""
    try:
        for pokemon in pokemon_list:
            if pokemon["id"] == id:
                return pokemon
        raise HTTPException(status_code=404, detail="Pokemon not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Pokémon: {str(e)}")

def add_new_pokemon(pokemon: Pokemon):
    """Add a new Pokémon to the list."""
    try:
        for p in pokemon_list:
            if p["id"] == pokemon.id:
                raise HTTPException(status_code=400, detail="Pokemon with this ID already exists")
        pokemon_list.append(pokemon.dict())
        pokemon_list.sort(key=lambda x: x["id"])
        save_pokemon_data(pokemon_list)
        return pokemon_list
    except HTTPException:
        raise  # Rethrow known exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding Pokémon: {str(e)}")

def update_existing_pokemon(id: int, updates: UpdatePokemon):
    """Update an existing Pokémon."""
    update_data = updates.model_dump(exclude_unset=True)  # Ensure valid data is extracted
    for pokemon in pokemon_list:
        if pokemon["id"] == id:
            for key, value in update_data.items():
                if key == "next_evolution":
                    pokemon[key] = [e.model_dump() for e in value]
                else:
                    pokemon[key] = value
            save_pokemon_data(pokemon_list)
            return {"message": "Pokemon updated successfully", "pokemon": pokemon}
    raise HTTPException(status_code=404, detail="Pokemon not found")
