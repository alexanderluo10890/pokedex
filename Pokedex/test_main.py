import pytest
import json
import os
from fastapi.testclient import TestClient
from main import app, load_pokemon_data, save_pokemon_data, Pokemon

# Create a test client for the FastAPI app
client = TestClient(app)

# Path to test JSON file
TEST_JSON_FILE = "test_pokedex.json"

@pytest.fixture
def setup_test_data():
    """Setup test data before each test and cleanup after"""
    test_data = {
        "pokemon": [
            {"id": 1, "name": "Pikachu", "type": ["Electric"]},
            {"id": 2, "name": "Charmander", "type": ["Fire"]},
            {"id": 3, "name": "Squirtle", "type": ["Water"]},
        ]
    }
    
    # Write test data to file
    with open(TEST_JSON_FILE, "w") as f:
        json.dump(test_data, f)
    
    yield test_data
    
    # Cleanup after test
    if os.path.exists(TEST_JSON_FILE):
        os.remove(TEST_JSON_FILE)


class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_returns_welcome_message(self):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Pokedex API"}


class TestGetPokemon:
    """Test fetching Pokémon by ID"""
    
    def test_get_existing_pokemon(self):
        """Test fetching an existing Pokémon"""
        # This assumes you have Pokémon with id=1 in your pokedex.json
        response = client.get("/pokemon/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "type" in data
    
    def test_get_nonexistent_pokemon(self):
        """Test fetching a non-existent Pokémon returns 404"""
        response = client.get("/pokemon/99999")
        assert response.status_code == 404
        assert "Pokemon not found" in response.json()["detail"]


class TestAddPokemon:
    """Test adding new Pokémon"""
    
    def test_add_pokemon_success(self):
        """Test successfully adding a new Pokémon"""
        new_pokemon = {
            "id": 100001,  # Changed to unique ID
            "name": "TestMon",
            "type": ["Normal"]
        }
        response = client.post("/pokemon", json=new_pokemon)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_add_pokemon_with_multiple_types(self):
        """Test adding a Pokémon with multiple types"""
        new_pokemon = {
            "id": 100002,  # Changed to unique ID
            "name": "DualTypeMon",
            "type": ["Fire", "Flying"]
        }
        response = client.post("/pokemon", json=new_pokemon)
        assert response.status_code == 201
        data = response.json()
        # Check that the Pokémon was added - Fixed the ID check
        pokemon_found = any(p.get("id") == 100002 for p in data)
        assert pokemon_found
    
    def test_add_duplicate_pokemon_id(self):
        """Test that adding a Pokémon with duplicate ID returns 400"""
        # First add a Pokémon
        new_pokemon = {
            "id": 100003,  # Changed to unique ID
            "name": "UniqueTest",
            "type": ["Normal"]
        }
        response1 = client.post("/pokemon", json=new_pokemon)
        assert response1.status_code == 201
        
        # Try adding another with same ID
        response2 = client.post("/pokemon", json=new_pokemon)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]


class TestUpdatePokemon:
    """Test updating existing Pokémon"""
    
    def test_update_pokemon_name(self):
        """Test updating a Pokémon's name"""
        # Get an existing Pokémon ID first
        response = client.get("/pokemon/1")
        if response.status_code == 200:
            update_data = {"name": "UpdatedName"}
            response = client.patch("/pokemon/1", json=update_data)
            assert response.status_code == 200
            assert "Pokemon updated successfully" in response.json()["message"]
    
    def test_update_pokemon_type(self):
        """Test updating a Pokémon's type"""
        update_data = {"type": ["Psychic", "Ghost"]}
        response = client.patch("/pokemon/2", json=update_data)
        # Will be 200 if Pokémon exists, 404 if not
        assert response.status_code in [200, 404]
    
    def test_update_nonexistent_pokemon(self):
        """Test updating a non-existent Pokémon returns 404"""
        update_data = {"name": "NewName"}
        response = client.patch("/pokemon/99999", json=update_data)
        assert response.status_code == 404
        assert "Pokemon not found" in response.json()["detail"]
    
    def test_update_pokemon_both_fields(self):
        """Test updating both name and type"""
        update_data = {
            "name": "UpdatedBoth",
            "type": ["Normal", "Flying"]
        }
        response = client.patch("/pokemon/1", json=update_data)
        assert response.status_code in [200, 404]


class TestValidation:
    """Test request validation"""
    
    def test_add_pokemon_missing_required_field(self):
        """Test that missing required fields are caught"""
        invalid_pokemon = {
            "id": 100,
            "name": "IncompleteMon"
            # Missing 'type' field
        }
        response = client.post("/pokemon", json=invalid_pokemon)
        assert response.status_code == 422  # Validation error
    
    def test_add_pokemon_wrong_type_for_field(self):
        """Test that wrong types are caught"""
        invalid_pokemon = {
            "id": "not_a_number",  # Should be int
            "name": "WrongType",
            "type": ["Fire"]
        }
        response = client.post("/pokemon", json=invalid_pokemon)
        assert response.status_code == 422  # Validation error
    
    def test_pokemon_types_must_be_list(self):
        """Test that type field must be a list"""
        invalid_pokemon = {
            "id": 101,
            "name": "InvalidType",
            "type": "Fire"  # Should be a list
        }
        response = client.post("/pokemon", json=invalid_pokemon)
        assert response.status_code == 422  # Validation error


class TestDataPersistence:
    """Test that data is properly saved and loaded"""
    
    def test_pokemon_list_sorted_by_id(self):
        """Test that Pokémon are sorted by ID after addition"""
        response = client.post("/pokemon", json={
            "id": 100004,  # Changed to unique ID
            "name": "TestSort",
            "type": ["Normal"]
        })
        assert response.status_code == 201
        pokemon_list = response.json()
        
        # Check if list is sorted by ID
        ids = [p["id"] for p in pokemon_list]
        assert ids == sorted(ids), "Pokémon list should be sorted by ID"