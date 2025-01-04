from fastapi import HTTPException
from app.utils.file_operations import load_pokemon_data, save_pokemon_data
from app.models.pokemon import Pokemon, UpdatePokemon, Evolution

# Load initial data
pokemon_list = load_pokemon_data()["pokemon"]

def get_pokemon_by_id(id: int):
    """Fetch a Pokémon by its ID."""
    try:
        for pokemon in pokemon_list:
            if pokemon["id"] == id:
                return pokemon
        raise HTTPException(status_code=404, detail="Pokemon not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Pokémon: {str(e)}")

def add_new_pokemon(pokemon: Pokemon):
    """Add a new Pokémon to the list."""
    try:
        for p in pokemon_list:
            if p["id"] == pokemon.id:
                raise HTTPException(status_code=400, detail="Pokemon with this ID already exists")
        pokemon_list.append(pokemon.model_dump())  # Changed from dict() to model_dump()
        pokemon_list.sort(key=lambda x: x["id"])
        save_pokemon_data(pokemon_list)
        return pokemon_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding Pokémon: {str(e)}")

def update_existing_pokemon(id: int, updates: UpdatePokemon):
    """Update an existing Pokémon."""
    update_data = updates.model_dump(exclude_unset=True)  # This was already using model_dump
    
    for pokemon in pokemon_list:
        if pokemon["id"] == id:
            # Handle evolution data specifically
            if "next_evolution" in update_data:
                if update_data["next_evolution"] is None:
                    pokemon["next_evolution"] = None
                else:
                    pokemon["next_evolution"] = [
                        Evolution(**evolution).model_dump()
                        for evolution in update_data["next_evolution"]
                    ]
                del update_data["next_evolution"]
                
            if "prev_evolution" in update_data:
                if update_data["prev_evolution"] is None:
                    pokemon["prev_evolution"] = None
                else:
                    pokemon["prev_evolution"] = [
                        Evolution(**evolution).model_dump()
                        for evolution in update_data["prev_evolution"]
                    ]
                del update_data["prev_evolution"]
            
            # Update remaining fields
            pokemon.update(update_data)
            save_pokemon_data(pokemon_list)
            return {"message": "Pokemon updated successfully", "pokemon": pokemon}
            
    raise HTTPException(status_code=404, detail="Pokemon not found")