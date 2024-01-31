# EGYGEO

EGYGEO is a Python package designed to provide easy access to the geographic coordinates (latitude and longitude) of various Egyptian subdivisions. It includes a module named `egysubdiv` that offers a convenient function, `get_coordinates`, allowing users to retrieve the geographic coordinates of a specified Egyptian subdivision by providing its name in either Arabic or English. The package supports the normalization of input subdivision names for robust matching.

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
