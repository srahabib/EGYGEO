# EGYGEO

EGYGEO is a Python package designed to provide easy access to the geographic coordinates (latitude and longitude) of various Egyptian subdivisions. It offers a function, `get_coordinates`, allowing users to retrieve the geographic coordinates of a specified Egyptian subdivision by providing its name in either Arabic or English.

## Installation

You can install egygeo using pip:

```bash
pip install egygeo
```

## Usage

```bash
from egygeo import get_coordinates

# Get coordinates for Cairo
latitude, longitude = get_coordinates('Cairo')
print(f"The coordinates of Cairo are: {latitude}, {longitude}")
```

```bash
from egygeo import get_name

lat, lon = 29.8951716, 31.1991806
location_name = get_name(lat, lon)
print(f"The subdivision at {lat}, {lon} is: {location_name}")
```
