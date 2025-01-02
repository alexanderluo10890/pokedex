import json
import os
from app.utils.file_operations import load_pokemon_data, save_pokemon_data
import threading
import time

def test_load_pokemon_data_success(mock_db_with_all_variants):
    """Test successfully loading pokemon data from file"""
    # mock_db_with_all_variants fixture creates a test file and returns the test data
    expected_data = mock_db_with_all_variants
    test_file = "test_pokedex.json"  # This is created by the fixture
    
    loaded_data = load_pokemon_data(test_file)
    
    # Verify we got the exact same data that was in the fixture
    assert loaded_data == expected_data
    
    # Additional specific checks for evolution patterns
    pokemon_names = {p["name"] for p in loaded_data["pokemon"]}
    expected_names = {"Bulbasaur", "Ditto", "Vaporeon"}
    assert pokemon_names == expected_names
    
    # Verify each evolution pattern
    for pokemon in loaded_data["pokemon"]:
        if pokemon["name"] == "Bulbasaur":
            assert "next_evolution" in pokemon
            assert "prev_evolution" not in pokemon
        elif pokemon["name"] == "Ditto":
            assert "next_evolution" not in pokemon
            assert "prev_evolution" not in pokemon
        elif pokemon["name"] == "Vaporeon":
            assert "prev_evolution" in pokemon
            assert "next_evolution" not in pokemon

def test_load_pokemon_data_file_not_found():
    """Test loading data when file doesn't exist"""
    nonexistent_file = "nonexistent_pokedex.json"
    
    # Make sure file doesn't exist
    if os.path.exists(nonexistent_file):
        os.remove(nonexistent_file)
    
    data = load_pokemon_data(nonexistent_file)
    assert data == {"pokemon": []}

def test_load_pokemon_data_invalid_json(test_db_file):
    """Test loading data from invalid JSON file"""
    # Write invalid JSON
    with open(test_db_file, "w") as f:
        f.write("This is not valid JSON")
    
    data = load_pokemon_data(test_db_file)
    assert data == {"pokemon": []}

def test_save_pokemon_data_success(test_db_file):
    """Test successfully saving pokemon data"""
    test_data = [
        {
            "id": 1,
            "name": "TestMon",
            "type": ["Test"]
        }
    ]
    
    save_pokemon_data(test_data, test_db_file)
    
    # Verify data was saved correctly
    with open(test_db_file, "r") as f:
        saved_data = json.load(f)
    
    assert "pokemon" in saved_data
    assert len(saved_data["pokemon"]) == 1
    assert saved_data["pokemon"][0]["name"] == "TestMon"

def test_save_pokemon_data_creates_file():
    """Test saving data creates file if it doesn't exist"""
    new_file = "new_test_pokedex.json"
    # Ensure file doesn't exist
    if os.path.exists(new_file):
        os.remove(new_file)
    
    try:
        test_data = [{"id": 1, "name": "TestMon"}]
        save_pokemon_data(test_data, new_file)
        
        assert os.path.exists(new_file)
        with open(new_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data["pokemon"] == test_data
    finally:
        # Cleanup
        if os.path.exists(new_file):
            os.remove(new_file)

def test_concurrent_file_access(test_db_file):
    """Test concurrent access to the file"""
    def save_operation(pokemon_data):
        save_pokemon_data(pokemon_data, test_db_file)
        time.sleep(0.1)  # Simulate some processing time
    
    # Create multiple threads to save data concurrently
    threads = []
    test_data = [
        [{"id": i, "name": f"TestMon{i}"}] for i in range(5)
    ]
    
    for data in test_data:
        thread = threading.Thread(target=save_operation, args=(data,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Verify file integrity
    with open(test_db_file, "r") as f:
        final_data = json.load(f)
    
    assert isinstance(final_data, dict)
    assert "pokemon" in final_data
    assert isinstance(final_data["pokemon"], list)

def test_save_pokemon_data_with_evolution_chains(test_db_file, ivysaur_data):
    """Test saving Pokemon with evolution chains"""
    save_pokemon_data([ivysaur_data], test_db_file)
    
    with open(test_db_file, "r") as f:
        saved_data = json.load(f)
    
    saved_pokemon = saved_data["pokemon"][0]
    assert "prev_evolution" in saved_pokemon
    assert "next_evolution" in saved_pokemon
    assert saved_pokemon["prev_evolution"][0]["name"] == "Bulbasaur"
    assert saved_pokemon["next_evolution"][0]["name"] == "Venusaur"

def test_empty_pokemon_list(test_db_file):
    """Test saving and loading empty Pokemon list"""
    save_pokemon_data([], test_db_file)
    
    data = load_pokemon_data(test_db_file)
    assert data == {"pokemon": []}