# Testing Concepts Overview

## Unit Testing

### What are Unit Tests?
Unit tests are a software testing method where individual components (units) of software are tested in isolation. A unit is typically the smallest testable part of an application, such as a function or method.

### Characteristics of Good Unit Tests
- **Isolated**: Tests should be independent and not rely on external systems or other tests
- **Repeatable**: Same results every time they run
- **Fast**: Quick to execute
- **Clear**: Easy to understand what's being tested
- **Single Responsibility**: Each test focuses on one specific functionality

## Types of Tests in Our Project

### 1. Model Tests
Tests that validate data structures and their behavior.
```python
def test_valid_pokemon_model():
    pokemon = Pokemon(id=1, name="Bulbasaur", ...)
    assert pokemon.id == 1
    assert pokemon.name == "Bulbasaur"
```

### 2. Service Tests
Tests that verify business logic and operations.
```python
def test_get_pokemon_by_id():
    pokemon = get_pokemon_by_id(1)
    assert pokemon["name"] == "Bulbasaur"
```

### 3. File Operation Tests
Tests that verify data persistence and file handling.
```python
def test_save_pokemon_data():
    save_pokemon_data([{"id": 1, "name": "Bulbasaur"}])
    assert file_exists("pokedex.json")
```

## Mocking

### What is Mocking?
Mocking is a technique used in unit testing where actual objects are replaced with mock objects that simulate their behavior. This is useful when:
- The real object is impractical to incorporate into a unit test
- The real object has non-deterministic behavior
- You want to verify how an object is being used

### Examples of Mocking in Our Tests
```python
# Mocking file operations
monkeypatch.setattr("app.services.pokemon_service.save_pokemon_data", 
                    lambda x: None)

# Mocking database data
monkeypatch.setattr(pokemon_service, "pokemon_list", 
                    mock_db_with_all_variants["pokemon"])
```

## Monkeypatching

### What is Monkeypatching?
Monkeypatching is a technique for modifying classes or modules in the runtime to change their behavior. In testing, we use it to:
- Replace functions with mock implementations
- Modify environment variables
- Change module-level variables

### Using pytest's monkeypatch
```python
def test_with_monkeypatch(monkeypatch):
    # Replace a function
    monkeypatch.setattr(module, "function_name", mock_function)
    
    # Set an environment variable
    monkeypatch.setenv("ENV_VAR", "test_value")
    
    # Modify a dictionary
    monkeypatch.setitem(some_dict, "key", "value")
```

## Test Fixtures

### What are Fixtures?
Fixtures are a way to provide a fixed baseline for tests. They:
- Set up test data
- Provide test dependencies
- Can be reused across multiple tests

### Example Fixtures from Our Project
```python
@pytest.fixture
def mock_db_with_all_variants():
    """Provides test database with different Pokemon types"""
    return {
        "pokemon": [
            {"name": "Bulbasaur", ...},
            {"name": "Ditto", ...},
            {"name": "Vaporeon", ...}
        ]
    }
```

## Test Organization

### Directory Structure
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_file_operations.py
└── conftest.py
```

### Shared Test Resources
- `conftest.py`: Contains shared fixtures
- Test data files
- Helper functions

## Test Coverage Types

### 1. Happy Path Testing
Testing the standard, expected flow:
```python
def test_add_new_pokemon_basic():
    """Test adding a valid new Pokemon"""
```

### 2. Error Path Testing
Testing error handling and edge cases:
```python
def test_add_duplicate_pokemon():
    """Test adding a Pokemon with existing ID"""
```

### 3. Edge Case Testing
Testing boundary conditions:
```python
def test_empty_pokemon_list():
    """Test handling empty Pokemon list"""
```

## Best Practices We Follow

1. **Clear Test Names**
   - Descriptive of what's being tested
   - Includes the scenario being tested

2. **Test Independence**
   - Each test can run in isolation
   - No dependencies between tests

3. **Arrange-Act-Assert Pattern**
   ```python
   # Arrange
   pokemon_data = {...}
   
   # Act
   result = add_new_pokemon(pokemon_data)
   
   # Assert
   assert result["name"] == "TestMon"
   ```

4. **Mock External Dependencies**
   - File system operations
   - Database calls
   - External services

5. **Clean Up After Tests**
   - Remove test files
   - Reset mocked states
   - Clean up any test data