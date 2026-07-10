"""
distance_calculator.py
──────────────────────
Geo-Optimization Engine  (Module 1)

Uses the Haversine formula to compute great‑circle distances between
a customer location and every warehouse, then returns a ranked list
sorted by proximity.
"""

from math import radians, sin, cos, sqrt, atan2
from typing import Dict, List, Tuple

EARTH_RADIUS_MI = 3958.8   # mean radius in statute miles


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth
    using the Haversine formula.

    Parameters
    ----------
    lat1, lon1 : float   — point A (degrees)
    lat2, lon2 : float   — point B (degrees)

    Returns
    -------
    float — distance in **miles**.
    """
    rlat1, rlon1 = radians(lat1), radians(lon1)
    rlat2, rlon2 = radians(lat2), radians(lon2)

    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1

    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_MI * c


class DistanceCalculator:
    """
    Ranks warehouses by straight-line distance to a customer location.

    Usage
    -----
    >>> calc = DistanceCalculator(warehouses)
    >>> ranked = calc.rank_warehouses(customer_lat, customer_lon)
    """

    def __init__(self, warehouses: List[Dict]):
        self.warehouses = warehouses

    def distance_to(self, customer_lat: float, customer_lon: float,
                    warehouse: Dict) -> float:
        """Return distance in miles from customer to a single warehouse."""
        return haversine(
            customer_lat, customer_lon,
            warehouse["lat"], warehouse["lon"],
        )

    def rank_warehouses(
        self,
        customer_lat: float,
        customer_lon: float,
        limit: int | None = None,
    ) -> List[Tuple[Dict, float]]:
        """
        Return warehouses sorted by ascending distance.

        Parameters
        ----------
        customer_lat, customer_lon : float
            Customer GPS coordinates.
        limit : int or None
            If set, return only the *limit* closest warehouses.

        Returns
        -------
        list of (warehouse_dict, distance_miles)
        """
        scored = [
            (wh, self.distance_to(customer_lat, customer_lon, wh))
            for wh in self.warehouses
        ]
        scored.sort(key=lambda x: x[1])

        if limit is not None:
            scored = scored[:limit]

        return scored

    def print_ranked(self, customer_lat: float, customer_lon: float,
                     top_n: int = 10):
        """Pretty-print the top-N nearest warehouses."""
        ranked = self.rank_warehouses(customer_lat, customer_lon, limit=top_n)
        print(f"\n{'Rank':<5} {'Warehouse':<30} {'City':<18} {'Dist (mi)':>10}")
        print("─" * 68)
        for i, (wh, dist) in enumerate(ranked, 1):
            print(f"{i:<5} {wh['name']:<30} {wh['city']:<18} {dist:>10.1f}")
