# dictdot

A Python library that provides dot-notation access to dictionary attributes.

## Installation

```bash
pip install dictdot
```

## Usage

```python
from dictdot import dotdict

# Create a dot-notation accessible dictionary
data = dotdict({
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

# Set values using dot notation
data.age = 31
data.address.zip = '12345'
```

## Features

- Dot-notation access to dictionary items
- Nested dictionary support
- Seamless integration with existing dictionaries
- Lightweight and dependency-free

## License

MIT
