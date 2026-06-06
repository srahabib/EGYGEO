import json
from functools import lru_cache
from pathlib import Path

import requests
from shapely.geometry import Point, shape

_DATA_DIR = Path(__file__).parent / "data"
DEFAULT_POINTS_PATH = str(_DATA_DIR / "Subdivisions_of_Egypt.json")
DEFAULT_BOUNDARIES_PATH = str(_DATA_DIR / "Governorate_boundaries.json")

# Alternate spellings and source-dataset names mapped to canonical English names.
NAME_ALIASES = {
    "alexandria": "Alexandria",
    "al iskandariyah": "Alexandria",
    "al iskandariyah governorate": "Alexandria",
    "alexandria governorate": "Alexandria",
    "الإسكندرية": "Alexandria",
    "الاسكندرية": "Alexandria",
    "aswan": "Aswan",
    "aswan governorate": "Aswan",
    "أسوان": "Aswan",
    "asyut": "Asyut",
    "asyut governorate": "Asyut",
    "assiut": "Asyut",
    "أسيوط": "Asyut",
    "beheira": "Beheira",
    "beheira governorate": "Beheira",
    "al buhayrah": "Beheira",
    "al buhayrah governorate": "Beheira",
    "البحيرة": "Beheira",
    "beni suef": "Beni Suef",
    "beni suef governorate": "Beni Suef",
    "bani suwayf": "Beni Suef",
    "بني سويف": "Beni Suef",
    "cairo": "Cairo",
    "cairo governorate": "Cairo",
    "al qahirah": "Cairo",
    "al qahirah governorate": "Cairo",
    "القاهرة": "Cairo",
    "dakahlia": "Dakahlia",
    "dakahlia governorate": "Dakahlia",
    "ad daqahliyah": "Dakahlia",
    "الدقهلية": "Dakahlia",
    "damietta": "Damietta",
    "damietta governorate": "Damietta",
    "dumyat": "Damietta",
    "دمياط": "Damietta",
    "faiyum": "Faiyum",
    "faiyum governorate": "Faiyum",
    "fayoum": "Faiyum",
    "al fayyum": "Faiyum",
    "الفيوم": "Faiyum",
    "gharbia": "Gharbia",
    "gharbiyya": "Gharbia",
    "gharbiyya governorate": "Gharbia",
    "al gharbiyah": "Gharbia",
    "الغربية": "Gharbia",
    "giza": "Giza",
    "giza governorate": "Giza",
    "al jizah": "Giza",
    "الجيزة": "Giza",
    "ismailia": "Ismailia",
    "ismailia governorate": "Ismailia",
    "al ismailiyah": "Ismailia",
    "الاسماعيلية": "Ismailia",
    "الإسماعيلية": "Ismailia",
    "kafr el sheikh": "Kafr El Sheikh",
    "kafr el-sheikh": "Kafr El Sheikh",
    "kafr el sheikh governorate": "Kafr El Sheikh",
    "kafr el-sheikh governorate": "Kafr El Sheikh",
    "kafr ash shaykh": "Kafr El Sheikh",
    "كفر الشيخ": "Kafr El Sheikh",
    "luxor": "Luxor",
    "luxor governate": "Luxor",
    "luxor governorate": "Luxor",
    "الأقصر": "Luxor",
    "matrouh": "Matrouh",
    "matrouh governorate": "Matrouh",
    "matruh": "Matrouh",
    "مطروح": "Matrouh",
    "minya": "Minya",
    "minya governate": "Minya",
    "minya governorate": "Minya",
    "al minya": "Minya",
    "المنيا": "Minya",
    "monufia": "Monufia",
    "monufia governorate": "Monufia",
    "al minufiyah": "Monufia",
    "المنوفية": "Monufia",
    "new valley": "New Valley",
    "new valley governorate": "New Valley",
    "al wadi al jadid": "New Valley",
    "الوادي الجديد": "New Valley",
    "north sinai": "North Sinai",
    "north sinai governorate": "North Sinai",
    "shamal sina": "North Sinai",
    "شمال سيناء": "North Sinai",
    "port said": "Port Said",
    "port said governorate": "Port Said",
    "bur said": "Port Said",
    "بورسعيد": "Port Said",
    "qalyubia": "Qalyubia",
    "qalyubia governorate": "Qalyubia",
    "al qalyubiyah": "Qalyubia",
    "القليوبية": "Qalyubia",
    "qena": "Qena",
    "qena governorate": "Qena",
    "قنا": "Qena",
    "red sea": "Red Sea",
    "red sea governorate": "Red Sea",
    "al bahr al ahmar": "Red Sea",
    "البحر الاحمر": "Red Sea",
    "البحر الأحمر": "Red Sea",
    "sharqia": "Sharqia",
    "sharqia governorate": "Sharqia",
    "al sharqia": "Sharqia",
    "al sharqia governorate": "Sharqia",
    "ash sharqiyah": "Sharqia",
    "الشرقية": "Sharqia",
    "sohag": "Sohag",
    "sohag governorate": "Sohag",
    "suhaj": "Sohag",
    "سوهاج": "Sohag",
    "south sinai": "South Sinai",
    "south sinai governorate": "South Sinai",
    "janub sina": "South Sinai",
    "جنوب سيناء": "South Sinai",
    "suez": "Suez",
    "suez governorate": "Suez",
    "as suways": "Suez",
    "السويس": "Suez",
}


def load_geojson_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)


def load_geojson(file_path_or_url):
    if file_path_or_url.startswith("http"):
        return load_geojson_from_url(file_path_or_url)
    with open(file_path_or_url, "r", encoding="utf-8") as geojson_file:
        return json.load(geojson_file)


@lru_cache(maxsize=8)
def _cached_geojson(file_path_or_url):
    return load_geojson(file_path_or_url)


@lru_cache(maxsize=8)
def _cached_boundary_shapes(file_path_or_url):
    geojson_data = _cached_geojson(file_path_or_url)
    indexed_shapes = []
    for feature in geojson_data["features"]:
        indexed_shapes.append(
            (shape(feature["geometry"]), feature.get("properties", {}))
        )
    return indexed_shapes


def _resolve_canonical_name(subdivision_name):
    normalized = subdivision_name.lower().strip()
    if normalized in NAME_ALIASES:
        return NAME_ALIASES[normalized]
    return subdivision_name.strip()


def _find_feature(subdivision_name, geojson_data):
    canonical_name = _resolve_canonical_name(subdivision_name)
    normalized_input = subdivision_name.lower().strip()
    canonical_lower = canonical_name.lower()

    for feature in geojson_data["features"]:
        properties = feature["properties"]
        english_name = properties.get("Subdivision_en", "").strip()
        arabic_name = properties.get("Subdivision_ar", "").strip()

        if canonical_lower == english_name.lower():
            return feature
        if normalized_input == arabic_name.lower():
            return feature
        if normalized_input == english_name.lower():
            return feature

    return None


def _properties_to_result(properties):
    return {
        "english": properties.get("Subdivision_en", ""),
        "arabic": properties.get("Subdivision_ar", ""),
        "id": properties.get("id"),
    }


def _point_from_feature(feature):
    geometry = feature["geometry"]
    if geometry["type"] == "Point" and len(geometry["coordinates"]) == 2:
        longitude, latitude = geometry["coordinates"]
        return latitude, longitude

    centroid = feature.get("properties", {}).get("centroid")
    if centroid and len(centroid) == 2:
        longitude, latitude = centroid
        return latitude, longitude

    return None


def list_governorates(geojson_path_or_url=DEFAULT_BOUNDARIES_PATH):
    """Return all governorates with English and Arabic names."""
    geojson_data = _cached_geojson(geojson_path_or_url)
    governorates = []
    for feature in geojson_data["features"]:
        properties = feature["properties"]
        governorates.append(_properties_to_result(properties))
    return sorted(governorates, key=lambda item: item["english"])


def get_coordinates(
    subdivision_name,
    geojson_path_or_url=DEFAULT_BOUNDARIES_PATH,
):
    """Return the centroid of a governorate as (latitude, longitude)."""
    geojson_data = _cached_geojson(geojson_path_or_url)
    feature = _find_feature(subdivision_name, geojson_data)
    if feature is None:
        return ()

    point = _point_from_feature(feature)
    if point is None:
        return ()

    return point


def get_boundary(
    subdivision_name,
    geojson_path_or_url=DEFAULT_BOUNDARIES_PATH,
    as_feature=False,
):
    """
    Return governorate border geometry.

    By default returns the GeoJSON geometry dict (Polygon or MultiPolygon).
    Set as_feature=True to return the full GeoJSON Feature, including properties.
    """
    geojson_data = _cached_geojson(geojson_path_or_url)
    feature = _find_feature(subdivision_name, geojson_data)
    if feature is None:
        return None

    geometry = feature["geometry"]
    if geometry["type"] not in ("Polygon", "MultiPolygon"):
        return None

    if as_feature:
        return feature
    return geometry


def get_geometry(
    subdivision_name,
    geometry_type="point",
    boundaries_path_or_url=DEFAULT_BOUNDARIES_PATH,
):
    """
    Return governorate geometry in the requested form.

    geometry_type:
      - "point": (latitude, longitude) centroid
      - "polygon": GeoJSON geometry dict
      - "feature": full GeoJSON Feature with polygon and properties
    """
    geometry_type = geometry_type.lower().strip()
    if geometry_type == "point":
        return get_coordinates(subdivision_name, boundaries_path_or_url)
    if geometry_type == "polygon":
        return get_boundary(subdivision_name, boundaries_path_or_url, as_feature=False)
    if geometry_type == "feature":
        return get_boundary(subdivision_name, boundaries_path_or_url, as_feature=True)
    raise ValueError('geometry_type must be "point", "polygon", or "feature"')


def get_name(
    latitude,
    longitude,
    geojson_path_or_url=DEFAULT_BOUNDARIES_PATH,
):
    """
    Find which governorate contains the given coordinate using point-in-polygon.

    Args:
        latitude: WGS84 latitude in decimal degrees.
        longitude: WGS84 longitude in decimal degrees.

    Returns:
        dict with english, arabic, and id keys, or None if not inside Egypt.
    """
    point = Point(longitude, latitude)
    for boundary_shape, properties in _cached_boundary_shapes(geojson_path_or_url):
        if boundary_shape.covers(point):
            return _properties_to_result(properties)
    return None


def draw_governorate(
    subdivision_name,
    output_path=None,
    zoom_start=10,
    fill_color="#3388ff",
    border_color="#1a1a1a",
    fill_opacity=0.35,
    line_weight=2,
    show_centroid=True,
    tile_style="OpenStreetMap",
    geojson_path_or_url=DEFAULT_BOUNDARIES_PATH,
):
    """
    Draw a governorate border on an interactive Folium map.

    Returns the Folium Map object. Saves to output_path when provided.

    Requires folium: pip install egygeo[map]
    """
    try:
        import folium
    except ImportError as exc:
        raise ImportError(
            "folium is required for draw_governorate. Install it with: pip install egygeo[map]"
        ) from exc

    feature = get_boundary(subdivision_name, geojson_path_or_url, as_feature=True)
    if feature is None:
        raise ValueError(f"Governorate not found: {subdivision_name}")

    centroid = _point_from_feature(feature)
    if centroid is None:
        raise ValueError(f"No centroid available for governorate: {subdivision_name}")

    latitude, longitude = centroid
    english_name = feature["properties"].get("Subdivision_en", subdivision_name)
    arabic_name = feature["properties"].get("Subdivision_ar", "")

    governorate_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=zoom_start,
        tiles=tile_style,
    )

    folium.GeoJson(
        feature,
        name=english_name,
        style_function=lambda _: {
            "fillColor": fill_color,
            "color": border_color,
            "weight": line_weight,
            "fillOpacity": fill_opacity,
        },
        tooltip=f"{english_name} ({arabic_name})",
    ).add_to(governorate_map)

    if show_centroid:
        folium.Marker(
            location=[latitude, longitude],
            popup=f"{english_name} centroid",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(governorate_map)

    folium.LayerControl().add_to(governorate_map)

    if output_path:
        governorate_map.save(output_path)

    return governorate_map
