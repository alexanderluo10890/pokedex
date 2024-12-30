from fastapi import APIRouter, HTTPException
from app.models.pokemon import Pokemon, UpdatePokemon
from app.services.pokemon_service import get_pokemon_by_id, add_new_pokemon, update_existing_pokemon

router = APIRouter()

@router.get("/{id}")
def get_pokemon(id: int):
    """Route to fetch a Pokémon by ID."""
    try:
        return get_pokemon_by_id(id)
    except HTTPException as e:
        raise e  # Rethrow known exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/", status_code=201)
def add_pokemon(pokemon: Pokemon):
    """Route to add a new Pokémon."""
    try:
        return add_new_pokemon(pokemon)
    except HTTPException as e:
        raise e  # Rethrow known exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.patch("/{id}")
def update_pokemon(id: int, updates: UpdatePokemon):
    """Route to update an existing Pokémon."""
    try:
        return update_existing_pokemon(id, updates)
    except HTTPException as e:
        raise e  # Rethrow known exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
