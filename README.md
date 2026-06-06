# EGYGEO

EGYGEO is a Python package for working with Egypt's 27 governorates. Look up centroids, retrieve border polygons, resolve any coordinate to its governorate using point-in-polygon, and draw interactive maps.

## Installation

```bash
pip install egygeo
```

For map drawing support:

```bash
pip install egygeo[map]
```

## Usage

### Get a governorate centroid

```python
from egygeo import get_coordinates

latitude, longitude = get_coordinates("Cairo")
print(f"Cairo centroid: {latitude}, {longitude}")

# Arabic names work too
latitude, longitude = get_coordinates("القاهرة")
```

### Get a governorate border

```python
from egygeo import get_boundary

cairo_border = get_boundary("Cairo")
cairo_feature = get_boundary("Cairo", as_feature=True)
```

### Reverse lookup — any point inside Egypt

`get_name` uses point-in-polygon against real governorate borders, so any coordinate inside a governorate works (not just centroids).

```python
from egygeo import get_name

# Pyramids of Giza area
result = get_name(29.9792, 31.1342)
print(result["english"])  # Giza
print(result["arabic"])   # الجيزة

# Downtown Cairo
result = get_name(30.0444, 31.2357)
print(result["english"])  # Cairo

# Returns None if the point is outside Egypt
result = get_name(40.7128, -74.0060)
print(result)  # None
```

### Draw a governorate on a map

```python
from egygeo import draw_governorate

draw_governorate("Alexandria", output_path="alexandria.html")
draw_governorate("Cairo", output_path="cairo.html", fill_color="#e74c3c")
```

### List all governorates

```python
from egygeo import list_governorates

for governorate in list_governorates():
    print(governorate["english"], governorate["arabic"])
```

### Unified geometry access

```python
from egygeo import get_geometry

point = get_geometry("Alexandria", geometry_type="point")
polygon = get_geometry("Alexandria", geometry_type="polygon")
feature = get_geometry("Alexandria", geometry_type="feature")
```

## Name matching

Governorate names can be provided in English or Arabic. Common alternate spellings from other datasets are also supported:

- `Cairo`, `Al Qahirah`, `القاهرة`
- `Alexandria`, `Al Iskandariyah`, `الإسكندرية`
- `Sharqia`, `Al Sharqia`, `الشرقية`
- `Kafr El Sheikh`, `Kafr el-Sheikh`, `كفر الشيخ`

## Data

Boundary polygons are sourced from [geoBoundaries](https://www.geoboundaries.org/) (CC BY 4.0 / ODbL) and normalized to use consistent `Subdivision_en` and `Subdivision_ar` property names across the package.
