import json
import threading
import logging

lock = threading.Lock()

def load_pokemon_data(filename: str = "pokedex.json"):
    """Load Pokémon data from the JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Pokemon file {filename} not found. Returning empty data.")
        return {"pokemon": []}
    except json.JSONDecodeError:
        logging.error(f"Malformed JSON in {filename}. Returning empty data.")
        return {"pokemon": []}

def save_pokemon_data(data, filename: str = "pokedex.json"):
    """Save Pokémon data to the JSON file."""
    with lock:
        try:
            with open(filename, "w") as file:
                json.dump({"pokemon": data}, file, indent=4)
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
            raise