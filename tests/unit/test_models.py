import pytest
from pydantic import ValidationError
from app.models.pokemon import Pokemon, Evolution, UpdatePokemon

def test_valid_evolution_model():
    """Test creating a valid Evolution model"""
    evolution_data = Evolution(
        num="002",
        name="Ivysaur"
    )
    assert evolution_data.num == "002"
    assert evolution_data.name == "Ivysaur"

def test_invalid_evolution_model():
    """Test Evolution model with missing required fields"""
    with pytest.raises(ValidationError):
        Evolution(name="Ivysaur")  # type: ignore # Missing num field

def test_valid_pokemon_model_with_next_evolution():
    """Test creating a Pokemon with next evolution (like Bulbasaur)"""
    pokemon_data = Pokemon(
        id=1,
        num="001",
        name="Bulbasaur",
        img="http://example.com/bulbasaur.jpg",
        type=["Grass", "Poison"],
        height="0.7 m",
        weight="6.9 kg",
        weaknesses=["Fire", "Ice", "Flying", "Psychic"],
        next_evolution=[
            Evolution(num="002", name="Ivysaur"),
            Evolution(num="003", name="Venusaur")
        ]
    )
    
    # Basic field assertions
    assert pokemon_data.id == 1
    assert pokemon_data.num == "001"
    assert pokemon_data.name == "Bulbasaur"
    assert pokemon_data.img == "http://example.com/bulbasaur.jpg"
    assert pokemon_data.height == "0.7 m"
    assert pokemon_data.weight == "6.9 kg"
    
    # List field assertions
    assert pokemon_data.type == ["Grass", "Poison"]
    assert pokemon_data.weaknesses == ["Fire", "Ice", "Flying", "Psychic"]
    
    # Evolution chain assertions
    assert pokemon_data.prev_evolution is None
    assert pokemon_data.next_evolution is not None  # First verify it's not None
    assert len(pokemon_data.next_evolution) == 2  # Then use len()
    
    # Verify first evolution
    assert pokemon_data.next_evolution[0].num == "002"
    assert pokemon_data.next_evolution[0].name == "Ivysaur"
    
    # Verify second evolution
    assert pokemon_data.next_evolution[1].num == "003"
    assert pokemon_data.next_evolution[1].name == "Venusaur"

def test_valid_pokemon_model_with_prev_evolution():
    """Test creating a Pokemon with prev evolution (like Vaporeon)"""
    pokemon_data = Pokemon(
        id=134,
        num="134",
        name="Vaporeon",
        img="http://example.com/vaporeon.jpg",
        type=["Water"],
        height="0.99 m",
        weight="29.0 kg",
        weaknesses=["Electric", "Grass"],
        prev_evolution=[
            Evolution(num="133", name="Eevee")
        ]
    )
    
    # Basic field assertions
    assert pokemon_data.id == 134
    assert pokemon_data.num == "134"
    assert pokemon_data.name == "Vaporeon"
    assert pokemon_data.img == "http://example.com/vaporeon.jpg"
    assert pokemon_data.height == "0.99 m"
    assert pokemon_data.weight == "29.0 kg"
    
    # List field assertions
    assert pokemon_data.type == ["Water"]
    assert pokemon_data.weaknesses == ["Electric", "Grass"]
    
    # Evolution chain assertions
    assert pokemon_data.next_evolution is None
    assert pokemon_data.prev_evolution is not None  # First verify it's not None
    assert len(pokemon_data.prev_evolution) == 1    # Then use len()
    
    # Verify previous evolution details
    assert pokemon_data.prev_evolution[0].num == "133"
    assert pokemon_data.prev_evolution[0].name == "Eevee"

def test_valid_pokemon_model_with_both_evolutions():
    """Test creating a Pokemon with both evolutions (like Ivysaur)"""
    pokemon_data = Pokemon(
        id=2,
        num="002",
        name="Ivysaur",
        img="http://example.com/ivysaur.jpg",
        type=["Grass", "Poison"],
        height="0.99 m",
        weight="13.0 kg",
        weaknesses=["Fire", "Ice", "Flying", "Psychic"],
        prev_evolution=[
            Evolution(num="001", name="Bulbasaur")
        ],
        next_evolution=[
            Evolution(num="003", name="Venusaur")
        ]
    )
    
    # Basic field assertions
    assert pokemon_data.id == 2
    assert pokemon_data.num == "002"
    assert pokemon_data.name == "Ivysaur"
    assert pokemon_data.img == "http://example.com/ivysaur.jpg"
    assert pokemon_data.height == "0.99 m"
    assert pokemon_data.weight == "13.0 kg"
    
    # List field assertions
    assert pokemon_data.type == ["Grass", "Poison"]
    assert pokemon_data.weaknesses == ["Fire", "Ice", "Flying", "Psychic"]
    
    # Evolution chain assertions
    assert pokemon_data.prev_evolution is not None
    assert pokemon_data.next_evolution is not None
    assert len(pokemon_data.prev_evolution) == 1
    assert len(pokemon_data.next_evolution) == 1
    
    # Verify previous evolution details
    assert pokemon_data.prev_evolution[0].num == "001"
    assert pokemon_data.prev_evolution[0].name == "Bulbasaur"
    
    # Verify next evolution details
    assert pokemon_data.next_evolution[0].num == "003"
    assert pokemon_data.next_evolution[0].name == "Venusaur"

def test_pokemon_model_without_evolution():
    """Test creating a Pokemon with no evolution (like Ditto)"""
    pokemon_data = Pokemon(
        id=132,
        num="132",
        name="Ditto",
        img="http://example.com/ditto.jpg",
        type=["Normal"],
        height="0.3 m",
        weight="4.0 kg",
        weaknesses=["Fighting"]
    )
    assert pokemon_data.next_evolution is None
    assert pokemon_data.prev_evolution is None

def test_invalid_pokemon_model():
    """Test Pokemon model with invalid or missing fields"""
    with pytest.raises(ValidationError):
        Pokemon(
            id="not_an_integer",  # Should be an integer
            name="Test",
            # Missing required fields
        ) # type: ignore

def test_valid_update_pokemon():
    """Test valid partial updates with UpdatePokemon model"""
    # Test basic field updates
    update_data = UpdatePokemon(
        name="Updated Name",
        weight="7.0 kg"
    )
    assert update_data.name == "Updated Name"
    assert update_data.weight == "7.0 kg"
    assert update_data.type is None  # Optional fields should be None if not provided

def test_update_pokemon_with_evolution():
    """Test updating Pokemon evolution data"""
    update_data = UpdatePokemon(
        next_evolution=[Evolution(num="002", name="NextForm")],
        prev_evolution=[Evolution(num="001", name="PrevForm")]
    )
    
    # Verify evolution chains exist
    assert update_data.next_evolution is not None
    assert update_data.prev_evolution is not None
    
    # Check lengths after null check
    assert len(update_data.next_evolution) == 1
    assert len(update_data.prev_evolution) == 1
    
    # Verify evolution details
    assert update_data.next_evolution[0].num == "002"
    assert update_data.next_evolution[0].name == "NextForm"
    assert update_data.prev_evolution[0].num == "001"
    assert update_data.prev_evolution[0].name == "PrevForm"
    
    # Verify other fields are None (partial update)
    assert update_data.name is None
    assert update_data.type is None
    assert update_data.weight is None
    assert update_data.height is None
    assert update_data.weaknesses is None

def test_update_pokemon_remove_evolution():
    """Test removing evolution data from Pokemon"""
    update_data = UpdatePokemon(
        next_evolution=None,
        prev_evolution=None
    )
    assert update_data.next_evolution is None
    assert update_data.prev_evolution is None

def test_update_pokemon_extra_fields():
    """Test UpdatePokemon rejects extra fields"""
    with pytest.raises(ValidationError):
        UpdatePokemon(
            name="Test",
            invalid_field="value"  # Extra field not in model # type: ignore
        )

def test_evolution_model_serialization():
    """Test Evolution model serialization"""
    evolution = Evolution(num="001", name="TestMon")
    serialized = evolution.model_dump()
    assert serialized == {"num": "001", "name": "TestMon"}

def test_pokemon_model_serialization():
    """Test Pokemon model serialization with evolution chains"""
    pokemon = Pokemon(
        id=1,
        num="001",
        name="TestMon",
        img="http://example.com/test.jpg",
        type=["Normal"],
        height="1.0 m",
        weight="10.0 kg",
        weaknesses=["Fighting"],
        next_evolution=[Evolution(num="002", name="NextForm")]
    )
    
    # Use exclude_none=True to exclude None values from the output
    serialized = pokemon.model_dump(exclude_none=True)
    
    # Verify evolution data
    assert serialized["next_evolution"][0]["name"] == "NextForm"
    assert "prev_evolution" not in serialized  # Now this will pass
    
    # Verify other fields
    assert serialized["id"] == 1
    assert serialized["name"] == "TestMon"
    assert serialized["type"] == ["Normal"]
    assert serialized["weaknesses"] == ["Fighting"]