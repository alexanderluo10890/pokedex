import pytest
import json
import os
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Test client for API endpoints"""
    return TestClient(app)

@pytest.fixture
def ditto_data():
    """Pokemon with no evolution"""
    return {
        "id": 132,
        "num": "132",
        "name": "Ditto",
        "img": "http://www.serebii.net/pokemongo/pokemon/132.png",
        "type": ["Normal"],
        "height": "0.30 m",
        "weight": "4.0 kg",
        "weaknesses": ["Fighting"]
    }

@pytest.fixture
def vaporeon_data():
    """Pokemon with only prev_evolution"""
    return {
        "id": 134,
        "num": "134",
        "name": "Vaporeon",
        "img": "http://www.serebii.net/pokemongo/pokemon/134.png",
        "type": ["Water"],
        "height": "0.99 m",
        "weight": "29.0 kg",
        "weaknesses": ["Electric", "Grass"],
        "prev_evolution": [
            {
                "num": "133",
                "name": "Eevee"
            }
        ]
    }

@pytest.fixture
def bulbasaur_data():
    """Pokemon with only next_evolution"""
    return {
        "id": 1,
        "num": "001",
        "name": "Bulbasaur",
        "img": "http://www.serebii.net/pokemongo/pokemon/001.png",
        "type": ["Grass", "Poison"],
        "height": "0.71 m",
        "weight": "6.9 kg",
        "weaknesses": ["Fire", "Ice", "Flying", "Psychic"],
        "next_evolution": [
            {
                "num": "002",
                "name": "Ivysaur"
            },
            {
                "num": "003",
                "name": "Venusaur"
            }
        ]
    }

@pytest.fixture
def ivysaur_data():
    """Pokemon with both prev_evolution and next_evolution"""
    return {
        "id": 2,
        "num": "002",
        "name": "Ivysaur",
        "img": "http://www.serebii.net/pokemongo/pokemon/002.png",
        "type": ["Grass", "Poison"],
        "height": "0.99 m",
        "weight": "13.0 kg",
        "weaknesses": ["Fire", "Ice", "Flying", "Psychic"],
        "prev_evolution": [
            {
                "num": "001",
                "name": "Bulbasaur"
            }
        ],
        "next_evolution": [
            {
                "num": "003",
                "name": "Venusaur"
            }
        ]
    }

@pytest.fixture
def test_db_file():
    """Create a temporary test database file"""
    filename = "test_pokedex.json"
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def mock_db_with_all_variants(test_db_file):
    """Create a test database with all Pokemon variants"""
    test_data = {
        "pokemon": [
            {
                "id": 1,
                "num": "001",
                "name": "Bulbasaur",
                "img": "http://www.serebii.net/pokemongo/pokemon/001.png",
                "type": ["Grass", "Poison"],
                "height": "0.71 m",
                "weight": "6.9 kg",
                "weaknesses": ["Fire", "Ice", "Flying", "Psychic"],
                "next_evolution": [
                    {
                        "num": "002",
                        "name": "Ivysaur"
                    }
                ]
            },
            {
                "id": 132,
                "num": "132",
                "name": "Ditto",
                "img": "http://www.serebii.net/pokemongo/pokemon/132.png",
                "type": ["Normal"],
                "height": "0.30 m",
                "weight": "4.0 kg",
                "weaknesses": ["Fighting"]
            },
            {
                "id": 134,
                "num": "134",
                "name": "Vaporeon",
                "img": "http://www.serebii.net/pokemongo/pokemon/134.png",
                "type": ["Water"],
                "height": "0.99 m",
                "weight": "29.0 kg",
                "weaknesses": ["Electric", "Grass"],
                "prev_evolution": [
                    {
                        "num": "133",
                        "name": "Eevee"
                    }
                ]
            }
        ]
    }
    with open(test_db_file, "w") as f:
        json.dump(test_data, f)
    return test_data

@pytest.fixture
def evolution_data():
    """Sample evolution data for testing"""
    return {
        "prev_evolution": [
            {
                "num": "001",
                "name": "PrevForm"
            }
        ],
        "next_evolution": [
            {
                "num": "003",
                "name": "NextForm"
            }
        ]
    }

@pytest.fixture
def invalid_evolution_data():
    """Invalid evolution data for testing validation"""
    return {
        "prev_evolution": [
            {
                "name": "MissingNum"  # Missing num field
            }
        ],
        "next_evolution": [
            {
                "num": "003"  # Missing name field
            }
        ]
    }

@pytest.fixture
def mock_pokemon_service(monkeypatch):
    """Mock the Pokemon service layer for testing"""
    class MockPokemonService:
        def __init__(self):
            self.pokemon_list = []

        def get_pokemon_by_id(self, id):
            for pokemon in self.pokemon_list:
                if pokemon["id"] == id:
                    return pokemon
            raise HTTPException(status_code=404, detail="Pokemon not found")

        def add_new_pokemon(self, pokemon):
            self.pokemon_list.append(pokemon.dict())
            return self.pokemon_list

        def update_existing_pokemon(self, id, updates):
            for pokemon in self.pokemon_list:
                if pokemon["id"] == id:
                    pokemon.update(updates.dict(exclude_unset=True))
                    return {"message": "Pokemon updated successfully", "pokemon": pokemon}
            raise HTTPException(status_code=404, detail="Pokemon not found")

    mock_service = MockPokemonService()
    monkeypatch.setattr("app.services.pokemon_service", mock_service)
    return mock_service

@pytest.fixture(autouse=True)
def reset_pokemon_service():
    """Reset pokemon service state before each test"""
    import app.services.pokemon_service as pokemon_service
    yield
    # Reset after each test
    pokemon_service.pokemon_list = pokemon_service.load_pokemon_data()["pokemon"]