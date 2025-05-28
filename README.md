# dictdot

A Python library that provides dot-notation access to dictionary attributes with safe handling of non-existent keys.

## Installation

```bash
pip install dictdot
```

## Usage

```python
from dictdot import Map

# Create a Map object
data = Map({
    'name': 'John',
    'age': 30,
    'address': {
        'street': '123 Main St',
        'city': 'Anytown'
    }
})

# Access using dot notation
print(data.name)  # John
print(data.address.city)  # Anytown

# Safe access to non-existent keys
print(data.non_existent)  # Returns an empty string when converted to string
print(repr(data.non_existent))  # Shows 'Map <non-existing>'

# Set values using dot notation
data.age = 31
data.address.zip = '12345'

# Nested assignment
data.some.nested.value = 'works'  # Creates the full path

# Dictionary-style access
print(data['name'])  # John

# Check if key exists
print('name' in data)  # True
print('non_existent' in data)  # False
```

## Features

- Dot-notation access to dictionary items
- Safe handling of non-existent keys (returns empty string when converted to string)
- Nested dictionary support with automatic path creation
- Dictionary-style access and methods (items(), keys())
- Merge functionality for combining dictionaries
- Lightweight and dependency-free

## Testing

The package includes a comprehensive test suite. To run the tests:

```bash
# Install test dependencies
pip install -e .[test]

# Run tests
pytest
```

## License

MIT
