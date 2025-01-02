import pytest
from fastapi import HTTPException
from app.services.pokemon_service import get_pokemon_by_id, add_new_pokemon, update_existing_pokemon
from app.models.pokemon import Pokemon, UpdatePokemon, Evolution

def test_get_pokemon_by_id_success(mock_db_with_all_variants, monkeypatch):
    """Test successfully getting different types of Pokemon"""
    # Mock the pokemon_list in the service module
    import app.services.pokemon_service as pokemon_service
    monkeypatch.setattr(pokemon_service, "pokemon_list", mock_db_with_all_variants["pokemon"])
    
    # Test getting Pokemon with next evolution
    bulbasaur = get_pokemon_by_id(1)
    assert bulbasaur["name"] == "Bulbasaur"
    assert "next_evolution" in bulbasaur
    assert len(bulbasaur["next_evolution"]) == 1
    assert bulbasaur["next_evolution"][0]["name"] == "Ivysaur"
    
    # Test getting Pokemon with no evolution
    ditto = get_pokemon_by_id(132)
    assert ditto["name"] == "Ditto"
    assert "next_evolution" not in ditto or ditto["next_evolution"] is None
    assert "prev_evolution" not in ditto or ditto["prev_evolution"] is None
    
    # Test getting Pokemon with prev evolution
    vaporeon = get_pokemon_by_id(134)
    assert vaporeon["name"] == "Vaporeon"
    assert "prev_evolution" in vaporeon
    assert len(vaporeon["prev_evolution"]) == 1
    assert vaporeon["prev_evolution"][0]["name"] == "Eevee"

def test_get_pokemon_not_found(mock_db_with_all_variants, monkeypatch):
    """Test getting a non-existent Pokemon"""
    import app.services.pokemon_service as pokemon_service
    monkeypatch.setattr(pokemon_service, "pokemon_list", mock_db_with_all_variants["pokemon"])
    
    with pytest.raises(HTTPException) as exc_info:
        get_pokemon_by_id(999)
    assert exc_info.value.status_code == 404
    assert "Pokemon not found" in str(exc_info.value.detail)

def test_add_new_pokemon_basic(mock_db_with_all_variants, monkeypatch):
    """Test adding a new Pokemon with no evolution"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    
    # Mock save_pokemon_data to do nothing - updated to accept both arguments
    monkeypatch.setattr("app.services.pokemon_service.save_pokemon_data", 
                       lambda x, filename=None: None)
    
    new_pokemon = Pokemon(
        id=150,
        num="150",
        name="Mewtwo",
        img="http://example.com/mewtwo.png",
        type=["Psychic"],
        height="2.0 m",
        weight="122.0 kg",
        weaknesses=["Dark", "Ghost", "Bug"]
    )
    
    result = add_new_pokemon(new_pokemon)
    added_pokemon = next(p for p in result if p["id"] == 150)
    assert added_pokemon["name"] == "Mewtwo"
    assert "next_evolution" not in added_pokemon or added_pokemon["next_evolution"] is None

def test_add_pokemon_with_evolution_chain(mock_db_with_all_variants, monkeypatch):
    """Test adding a Pokemon with evolution chain"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    
    # Mock save_pokemon_data to do nothing - updated to accept both arguments
    monkeypatch.setattr("app.services.pokemon_service.save_pokemon_data", 
                       lambda x, filename=None: None)
    
    new_pokemon = Pokemon(
        id=150,
        num="150",
        name="Mewtwo",
        img="http://example.com/mewtwo.png",
        type=["Psychic"],
        height="2.0 m",
        weight="122.0 kg",
        weaknesses=["Dark", "Ghost", "Bug"],
        prev_evolution=[Evolution(num="149", name="PreForm")],
        next_evolution=[Evolution(num="151", name="NextForm")]
    )
    
    result = add_new_pokemon(new_pokemon)
    added_pokemon = next(p for p in result if p["id"] == 150)
    assert added_pokemon["prev_evolution"][0]["name"] == "PreForm"
    assert added_pokemon["next_evolution"][0]["name"] == "NextForm"

def test_add_duplicate_pokemon(mock_db_with_all_variants, monkeypatch):
    """Test adding a Pokemon with existing ID"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    
    duplicate_pokemon = Pokemon(
        id=132,  # Ditto's ID
        num="132",
        name="Duplicate",
        img="http://example.com/ditto.jpg",
        type=["Normal"],
        height="0.3 m",
        weight="4.0 kg",
        weaknesses=["Fighting"]
    )
    
    with pytest.raises(HTTPException) as exc_info:
        add_new_pokemon(duplicate_pokemon)
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail).lower()

def test_update_pokemon_basic_info(mock_db_with_all_variants, monkeypatch):
    """Test updating basic Pokemon information"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    
    # Mock save_pokemon_data to do nothing
    monkeypatch.setattr("app.services.pokemon_service.save_pokemon_data", lambda x: None)
    
    updates = UpdatePokemon(
        name="Updated Ditto",
        weight="5.0 kg"
    )
    
    result = update_existing_pokemon(132, updates)
    assert result["pokemon"]["name"] == "Updated Ditto"
    assert result["pokemon"]["weight"] == "5.0 kg"
    assert result["pokemon"]["type"] == ["Normal"]  # Original field unchanged

def test_update_pokemon_evolution(mock_db_with_all_variants, monkeypatch):
    """Test updating Pokemon evolution data"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    monkeypatch.setattr("app.services.pokemon_service.save_pokemon_data", lambda x: None)
    
    updates = UpdatePokemon(
        next_evolution=[Evolution(num="133", name="NewEvolution")]
    )
    
    result = update_existing_pokemon(132, updates)  # Update Ditto
    assert "next_evolution" in result["pokemon"]
    assert result["pokemon"]["next_evolution"][0]["name"] == "NewEvolution"

def test_update_pokemon_remove_evolution(mock_db_with_all_variants, monkeypatch):
    """Test removing evolution from Pokemon"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    monkeypatch.setattr("app.services.pokemon_service.save_pokemon_data", lambda x: None)
    
    updates = UpdatePokemon(prev_evolution=None)
    result = update_existing_pokemon(134, updates)  # Update Vaporeon
    assert "prev_evolution" not in result["pokemon"] or result["pokemon"]["prev_evolution"] is None

def test_update_nonexistent_pokemon(mock_db_with_all_variants, monkeypatch):
    """Test updating a Pokemon that doesn't exist"""
    import app.services.pokemon_service as pokemon_service
    test_list = mock_db_with_all_variants["pokemon"].copy()
    monkeypatch.setattr(pokemon_service, "pokemon_list", test_list)
    
    updates = UpdatePokemon(name="Test")
    with pytest.raises(HTTPException) as exc_info:
        update_existing_pokemon(999, updates)
    assert exc_info.value.status_code == 404