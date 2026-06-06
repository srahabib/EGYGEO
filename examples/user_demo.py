"""
Run this script as an egygeo user would:

    pip install -e ".[map]"
    python examples/user_demo.py

It prints API results to the terminal and saves HTML maps you can open
in a browser to visually check governorate borders.
"""

import sys
from pathlib import Path

# Keep Arabic output readable on Windows terminals.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from egygeo import (
    draw_governorate,
    get_boundary,
    get_coordinates,
    get_geometry,
    get_name,
    list_governorates,
)

OUTPUT_DIR = Path(__file__).parent / "output"


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def check(label, condition):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    return condition


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_passed = True

    section("1. List all governorates")
    governorates = list_governorates()
    all_passed &= check(f"Egypt has 27 governorates (got {len(governorates)})", len(governorates) == 27)
    print(f"  First 3: {[g['english'] for g in governorates[:3]]}")
    print(f"  Last 3:  {[g['english'] for g in governorates[-3:]]}")

    section("2. Get centroids (latitude, longitude)")
    test_governorates = ["Cairo", "Alexandria", "Giza", "الأقصر"]
    for name in test_governorates:
        lat, lon = get_coordinates(name)
        ok = bool(lat and lon)
        all_passed &= check(f"{name!r} -> ({lat}, {lon})", ok)
        if ok:
            print(f"         lat={lat:.4f}, lon={lon:.4f}")

    section("3. Get border polygons")
    for name in ["Cairo", "Alexandria", "South Sinai"]:
        geometry = get_boundary(name)
        ok = geometry is not None and geometry["type"] in ("Polygon", "MultiPolygon")
        all_passed &= check(f"{name} border is {geometry['type'] if geometry else 'missing'}", ok)

    feature = get_geometry("Cairo", geometry_type="feature")
    all_passed &= check(
        "Feature includes english + arabic names",
        feature["properties"]["Subdivision_en"] == "Cairo"
        and feature["properties"]["Subdivision_ar"] == "القاهرة",
    )

    section("4. Reverse lookup — point inside governorate borders")
    # (latitude, longitude, expected_english_name, description)
    landmark_tests = [
        (30.0444, 31.2357, "Cairo", "Downtown Cairo"),
        (29.9792, 31.1342, "Giza", "Giza Pyramids area"),
        (31.2001, 29.9187, "Alexandria", "Alexandria waterfront"),
        (25.6872, 32.6396, "Luxor", "Luxor Temple area"),
        (27.2579, 33.8116, "Red Sea", "Hurghada coast"),
        (29.9745, 32.5371, "Suez", "Suez city center"),
    ]
    for lat, lon, expected, description in landmark_tests:
        result = get_name(lat, lon)
        ok = result is not None and result["english"] == expected
        all_passed &= check(f"{description} -> {expected}", ok)
        if result:
            print(f"         got: {result['english']} / {result['arabic']}")

    section("5. Point outside Egypt returns None")
    result = get_name(40.7128, -74.0060)  # New York
    all_passed &= check("New York -> None", result is None)

    section("6. Name aliases still work")
    alias_tests = [
        ("Al Qahirah", "Cairo"),
        ("Al Iskandariyah", "Alexandria"),
        ("Gharbiyya", "Gharbia"),
        ("Kafr el-Sheikh", "Kafr El Sheikh"),
    ]
    for alias, expected in alias_tests:
        lat_lon = get_coordinates(alias)
        ok = bool(lat_lon) and get_boundary(alias) is not None
        all_passed &= check(f"{alias!r} resolves like {expected}", ok)

    section("7. Draw maps — open these HTML files in your browser")
    maps_to_draw = [
        ("Cairo", "cairo_map.html", "#e74c3c"),
        ("Alexandria", "alexandria_map.html", "#3498db"),
        ("Giza", "giza_map.html", "#f39c12"),
    ]
    for name, filename, color in maps_to_draw:
        output_path = OUTPUT_DIR / filename
        draw_governorate(name, output_path=str(output_path), fill_color=color)
        print(f"  Saved: {output_path}")

    # All governorates on one map for a full-country border check
    all_egypt_path = OUTPUT_DIR / "all_egypt_map.html"
    _draw_all_egypt(all_egypt_path)
    print(f"  Saved: {all_egypt_path}")

    section("RESULT")
    if all_passed:
        print("  All checks passed.")
        print()
        print("  Next step: open the HTML files in examples/output/ in your browser")
        print("  and confirm the colored borders line up with the real governorates.")
    else:
        print("  Some checks failed — review the output above.")
        raise SystemExit(1)


def _draw_all_egypt(output_path):
    """Build one map with every governorate outline for visual inspection."""
    import folium

    features = [
        get_geometry(governorate["english"], geometry_type="feature")
        for governorate in list_governorates()
    ]
    geojson_data = {"type": "FeatureCollection", "features": features}

    egypt_map = folium.Map(location=[26.8, 30.8], zoom_start=6, tiles="OpenStreetMap")

    folium.GeoJson(
        geojson_data,
        name="All governorates",
        style_function=lambda feature: {
            "fillColor": _color_for_id(feature["properties"].get("id", 0)),
            "color": "#333333",
            "weight": 1,
            "fillOpacity": 0.4,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Subdivision_en", "Subdivision_ar"],
            aliases=["English:", "Arabic:"],
        ),
    ).add_to(egypt_map)

    folium.LayerControl().add_to(egypt_map)
    egypt_map.save(str(output_path))


def _color_for_id(gov_id):
    palette = [
        "#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
        "#1abc9c", "#e67e22", "#34495e", "#16a085", "#c0392b",
    ]
    return palette[(gov_id - 1) % len(palette)]


if __name__ == "__main__":
    main()
