"""
shipping_service.py
───────────────────
Shipping & Carrier Optimization  (Module 4)

Mock API classes for FedEx and UPS that return estimated shipping cost
and delivery time based on distance (miles) and weight (lbs).
A composite ShippingService compares carriers and picks the best one.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ShippingQuote:
    """Immutable quote from a shipping carrier."""
    carrier: str
    cost: float          # USD
    delivery_days: int   # estimated business days
    service_level: str   # e.g. "Ground", "Express"

    def score(self, cost_weight: float = 0.6, time_weight: float = 0.4) -> float:
        """
        Lower is better.
        Weighted composite of normalised cost & time so the caller can
        tune the tradeoff between speed and price.
        """
        return cost_weight * self.cost + time_weight * (self.delivery_days * 10)

    def to_dict(self) -> Dict:
        return {
            "carrier": self.carrier,
            "service_level": self.service_level,
            "cost_usd": round(self.cost, 2),
            "estimated_delivery_days": self.delivery_days,
        }


# ═══════════════════════════════════════════════════════════════════════════
# Mock Carrier APIs
# ═══════════════════════════════════════════════════════════════════════════

class FedExAPI:
    """
    Mock FedEx shipping API.

    Pricing model (simplified):
      base  = $4.99
      per‑mile  = $0.012
      per‑lb    = $0.85
      Express multiplier = 1.8×, shaves 2 days off Ground.
    """
    CARRIER = "FedEx"
    BASE_RATE = 4.99
    PER_MILE  = 0.012
    PER_LB    = 0.85

    def get_quote(self, distance_mi: float, weight_lbs: float,
                  express: bool = False) -> ShippingQuote:
        cost = self.BASE_RATE + distance_mi * self.PER_MILE + weight_lbs * self.PER_LB
        days = max(1, int(distance_mi / 600) + 1)   # ~600 mi/day ground

        if express:
            cost *= 1.8
            days = max(1, days - 2)
            level = "FedEx Express"
        else:
            level = "FedEx Ground"

        return ShippingQuote(
            carrier=self.CARRIER,
            cost=round(cost, 2),
            delivery_days=days,
            service_level=level,
        )


class UPSAPI:
    """
    Mock UPS shipping API.

    Pricing model (simplified):
      base  = $5.49
      per‑mile  = $0.010
      per‑lb    = $0.78
      Next‑Day Air multiplier = 2.1×, guaranteed 1‑2 days.
    """
    CARRIER = "UPS"
    BASE_RATE = 5.49
    PER_MILE  = 0.010
    PER_LB    = 0.78

    def get_quote(self, distance_mi: float, weight_lbs: float,
                  express: bool = False) -> ShippingQuote:
        cost = self.BASE_RATE + distance_mi * self.PER_MILE + weight_lbs * self.PER_LB
        days = max(1, int(distance_mi / 550) + 1)   # slightly slower ground

        if express:
            cost *= 2.1
            days = min(2, days)
            level = "UPS Next Day Air"
        else:
            level = "UPS Ground"

        return ShippingQuote(
            carrier=self.CARRIER,
            cost=round(cost, 2),
            delivery_days=days,
            service_level=level,
        )


# ═══════════════════════════════════════════════════════════════════════════
# Composite Shipping Service
# ═══════════════════════════════════════════════════════════════════════════

class ShippingService:
    """
    Aggregates quotes from all carriers and selects the optimal one.

    Parameters
    ----------
    cost_weight : float
        Importance of cost in the composite score (0‑1).
    time_weight : float
        Importance of delivery speed (0‑1).
    """

    def __init__(self, cost_weight: float = 0.6, time_weight: float = 0.4):
        self.fedex = FedExAPI()
        self.ups   = UPSAPI()
        self.cost_weight = cost_weight
        self.time_weight = time_weight

    def get_all_quotes(self, distance_mi: float,
                       weight_lbs: float) -> List[ShippingQuote]:
        """Return quotes from every carrier × service level."""
        return [
            self.fedex.get_quote(distance_mi, weight_lbs, express=False),
            self.fedex.get_quote(distance_mi, weight_lbs, express=True),
            self.ups.get_quote(distance_mi, weight_lbs, express=False),
            self.ups.get_quote(distance_mi, weight_lbs, express=True),
        ]

    def best_quote(self, distance_mi: float,
                   weight_lbs: float) -> ShippingQuote:
        """Select the carrier with the best composite score."""
        quotes = self.get_all_quotes(distance_mi, weight_lbs)
        return min(
            quotes,
            key=lambda q: q.score(self.cost_weight, self.time_weight),
        )

    def compare_quotes(self, distance_mi: float,
                       weight_lbs: float) -> List[Dict]:
        """Return all quotes as dicts for reporting / JSON output."""
        quotes = self.get_all_quotes(distance_mi, weight_lbs)
        quotes.sort(key=lambda q: q.score(self.cost_weight, self.time_weight))
        return [
            {**q.to_dict(), "composite_score": round(q.score(self.cost_weight, self.time_weight), 2)}
            for q in quotes
        ]
