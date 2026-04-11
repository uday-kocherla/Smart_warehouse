"""
warehouse_data.py
─────────────────
Generates mock data for 50 US warehouses spread across the country.
Each warehouse has:
  • name, city, state
  • latitude / longitude
  • inventory levels for 5 sample products
  • a max‑capacity field (units)
"""

import csv
import random
import os
from typing import Dict, List

# ── 50 realistic US warehouse locations ──────────────────────────────────────

WAREHOUSE_SEED: List[Dict] = [
    {"id": "WH-001", "name": "Los Angeles DC",        "city": "Los Angeles",     "state": "CA", "lat": 33.9425, "lon": -118.4081},
    {"id": "WH-002", "name": "Chicago Hub",           "city": "Chicago",         "state": "IL", "lat": 41.8781, "lon": -87.6298},
    {"id": "WH-003", "name": "Houston Mega",          "city": "Houston",         "state": "TX", "lat": 29.7604, "lon": -95.3698},
    {"id": "WH-004", "name": "Phoenix West",          "city": "Phoenix",         "state": "AZ", "lat": 33.4484, "lon": -112.0740},
    {"id": "WH-005", "name": "Philadelphia East",     "city": "Philadelphia",    "state": "PA", "lat": 39.9526, "lon": -75.1652},
    {"id": "WH-006", "name": "San Antonio South",     "city": "San Antonio",     "state": "TX", "lat": 29.4241, "lon": -98.4936},
    {"id": "WH-007", "name": "San Diego Coastal",     "city": "San Diego",       "state": "CA", "lat": 32.7157, "lon": -117.1611},
    {"id": "WH-008", "name": "Dallas Central",        "city": "Dallas",          "state": "TX", "lat": 32.7767, "lon": -96.7970},
    {"id": "WH-009", "name": "San Jose Tech",         "city": "San Jose",        "state": "CA", "lat": 37.3382, "lon": -121.8863},
    {"id": "WH-010", "name": "Austin Metro",          "city": "Austin",          "state": "TX", "lat": 30.2672, "lon": -97.7431},
    {"id": "WH-011", "name": "Jacksonville Port",     "city": "Jacksonville",    "state": "FL", "lat": 30.3322, "lon": -81.6557},
    {"id": "WH-012", "name": "Columbus Midwest",      "city": "Columbus",        "state": "OH", "lat": 39.9612, "lon": -82.9988},
    {"id": "WH-013", "name": "Charlotte Southeast",   "city": "Charlotte",       "state": "NC", "lat": 35.2271, "lon": -80.8431},
    {"id": "WH-014", "name": "Indianapolis Cross",    "city": "Indianapolis",    "state": "IN", "lat": 39.7684, "lon": -86.1581},
    {"id": "WH-015", "name": "San Francisco Bay",     "city": "San Francisco",   "state": "CA", "lat": 37.7749, "lon": -122.4194},
    {"id": "WH-016", "name": "Seattle Pacific",       "city": "Seattle",         "state": "WA", "lat": 47.6062, "lon": -122.3321},
    {"id": "WH-017", "name": "Denver Mountain",       "city": "Denver",          "state": "CO", "lat": 39.7392, "lon": -104.9903},
    {"id": "WH-018", "name": "Washington DC Metro",   "city": "Washington",      "state": "DC", "lat": 38.9072, "lon": -77.0369},
    {"id": "WH-019", "name": "Nashville Music",       "city": "Nashville",       "state": "TN", "lat": 36.1627, "lon": -86.7816},
    {"id": "WH-020", "name": "Oklahoma City Plains",  "city": "Oklahoma City",   "state": "OK", "lat": 35.4676, "lon": -97.5164},
    {"id": "WH-021", "name": "El Paso Border",        "city": "El Paso",         "state": "TX", "lat": 31.7619, "lon": -106.4850},
    {"id": "WH-022", "name": "Boston Harbor",         "city": "Boston",          "state": "MA", "lat": 42.3601, "lon": -71.0589},
    {"id": "WH-023", "name": "Portland Green",        "city": "Portland",        "state": "OR", "lat": 45.5152, "lon": -122.6784},
    {"id": "WH-024", "name": "Las Vegas Desert",      "city": "Las Vegas",       "state": "NV", "lat": 36.1699, "lon": -115.1398},
    {"id": "WH-025", "name": "Memphis River",         "city": "Memphis",         "state": "TN", "lat": 35.1495, "lon": -90.0490},
    {"id": "WH-026", "name": "Louisville Derby",      "city": "Louisville",      "state": "KY", "lat": 38.2527, "lon": -85.7585},
    {"id": "WH-027", "name": "Baltimore Harbor",      "city": "Baltimore",       "state": "MD", "lat": 39.2904, "lon": -76.6122},
    {"id": "WH-028", "name": "Milwaukee Lake",        "city": "Milwaukee",       "state": "WI", "lat": 43.0389, "lon": -87.9065},
    {"id": "WH-029", "name": "Albuquerque Mesa",      "city": "Albuquerque",     "state": "NM", "lat": 35.0844, "lon": -106.6504},
    {"id": "WH-030", "name": "Tucson Sonoran",        "city": "Tucson",          "state": "AZ", "lat": 32.2226, "lon": -110.9747},
    {"id": "WH-031", "name": "Fresno Valley",         "city": "Fresno",          "state": "CA", "lat": 36.7378, "lon": -119.7871},
    {"id": "WH-032", "name": "Sacramento Capital",    "city": "Sacramento",      "state": "CA", "lat": 38.5816, "lon": -121.4944},
    {"id": "WH-033", "name": "Kansas City Gateway",   "city": "Kansas City",     "state": "MO", "lat": 39.0997, "lon": -94.5786},
    {"id": "WH-034", "name": "Atlanta Peach",         "city": "Atlanta",         "state": "GA", "lat": 33.7490, "lon": -84.3880},
    {"id": "WH-035", "name": "Omaha Heartland",       "city": "Omaha",           "state": "NE", "lat": 41.2565, "lon": -95.9345},
    {"id": "WH-036", "name": "Miami Tropical",        "city": "Miami",           "state": "FL", "lat": 25.7617, "lon": -80.1918},
    {"id": "WH-037", "name": "Raleigh Research",      "city": "Raleigh",         "state": "NC", "lat": 35.7796, "lon": -78.6382},
    {"id": "WH-038", "name": "Minneapolis Twin",      "city": "Minneapolis",     "state": "MN", "lat": 44.9778, "lon": -93.2650},
    {"id": "WH-039", "name": "Tampa Bay",             "city": "Tampa",           "state": "FL", "lat": 27.9506, "lon": -82.4572},
    {"id": "WH-040", "name": "New Orleans Delta",     "city": "New Orleans",     "state": "LA", "lat": 29.9511, "lon": -90.0715},
    {"id": "WH-041", "name": "Cleveland Steel",       "city": "Cleveland",       "state": "OH", "lat": 41.4993, "lon": -81.6944},
    {"id": "WH-042", "name": "Pittsburgh Iron",       "city": "Pittsburgh",      "state": "PA", "lat": 40.4406, "lon": -79.9959},
    {"id": "WH-043", "name": "St. Louis Arch",        "city": "St. Louis",       "state": "MO", "lat": 38.6270, "lon": -90.1994},
    {"id": "WH-044", "name": "Cincinnati Queen",      "city": "Cincinnati",      "state": "OH", "lat": 39.1031, "lon": -84.5120},
    {"id": "WH-045", "name": "Salt Lake Summit",      "city": "Salt Lake City",  "state": "UT", "lat": 40.7608, "lon": -111.8910},
    {"id": "WH-046", "name": "Detroit Motor",         "city": "Detroit",         "state": "MI", "lat": 42.3314, "lon": -83.0458},
    {"id": "WH-047", "name": "New York Metro",        "city": "New York",        "state": "NY", "lat": 40.7128, "lon": -74.0060},
    {"id": "WH-048", "name": "Boise Gem",             "city": "Boise",           "state": "ID", "lat": 43.6150, "lon": -116.2023},
    {"id": "WH-049", "name": "Richmond Capital",      "city": "Richmond",        "state": "VA", "lat": 37.5407, "lon": -77.4360},
    {"id": "WH-050", "name": "Honolulu Island",       "city": "Honolulu",        "state": "HI", "lat": 21.3069, "lon": -157.8583},
]

# ── 5 sample products ───────────────────────────────────────────────────────

PRODUCTS = [
    {"sku": "SKU-A100", "name": "Wireless Bluetooth Headphones", "weight_lbs": 0.6},
    {"sku": "SKU-B200", "name": "Portable Power Bank 20000mAh",  "weight_lbs": 1.1},
    {"sku": "SKU-C300", "name": "Smart Home Security Camera",    "weight_lbs": 1.8},
    {"sku": "SKU-D400", "name": "Ergonomic Mechanical Keyboard",  "weight_lbs": 2.4},
    {"sku": "SKU-E500", "name": "USB-C Docking Station",          "weight_lbs": 3.2},
]


def generate_warehouse_data(seed: int = 42) -> List[Dict]:
    """
    Returns a list of 50 warehouse dicts, each augmented with random inventory
    levels for every product SKU.

    Parameters
    ----------
    seed : int
        Random seed for reproducibility.
    """
    rng = random.Random(seed)
    warehouses = []

    for wh in WAREHOUSE_SEED:
        record = dict(wh)
        record["max_capacity"] = rng.randint(5000, 20000)
        record["inventory"] = {}
        for prod in PRODUCTS:
            record["inventory"][prod["sku"]] = rng.randint(0, 500)
        warehouses.append(record)

    return warehouses


def export_warehouses_csv(warehouses: List[Dict], filepath: str = "warehouses.csv"):
    """Export warehouse data to a CSV file for inspection."""
    fieldnames = [
        "id", "name", "city", "state", "lat", "lon", "max_capacity",
    ] + [p["sku"] for p in PRODUCTS]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for wh in warehouses:
            row = {
                "id": wh["id"],
                "name": wh["name"],
                "city": wh["city"],
                "state": wh["state"],
                "lat": wh["lat"],
                "lon": wh["lon"],
                "max_capacity": wh["max_capacity"],
            }
            for prod in PRODUCTS:
                row[prod["sku"]] = wh["inventory"][prod["sku"]]
            writer.writerow(row)

    print(f"[✓] Exported {len(warehouses)} warehouses → {os.path.abspath(filepath)}")


if __name__ == "__main__":
    data = generate_warehouse_data()
    export_warehouses_csv(data)
    # quick sanity print
    for w in data[:3]:
        print(f"  {w['id']}  {w['name']:30s}  inv={w['inventory']}")
