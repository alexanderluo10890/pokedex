import json
import threading
import logging

lock = threading.Lock()

def load_pokemon_data():
    """Load Pokémon data from the JSON file."""
    try:
        with open("pokedex.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Pokedex file not found. Returning empty data.")
        return {"pokemon": []}
    except json.JSONDecodeError:
        logging.error("Malformed JSON in pokedex.json. Returning empty data.")
        return {"pokemon": []}

def save_pokemon_data(data):
    """Save Pokémon data to the JSON file."""
    with lock:
        try:
            with open("pokedex.json", "w") as file:
                json.dump({"pokemon": data}, file, indent=4)
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
            raise
