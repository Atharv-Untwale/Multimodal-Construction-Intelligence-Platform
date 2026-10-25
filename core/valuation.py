"""Project budget and real estate valuation engine (INR)."""
from __future__ import annotations
from dataclasses import dataclass

from core.config import (CONTINGENCY_PCT, LAND_VALUE_SHARE, LOCATION_TIERS, MILESTONES, STRUCTURE_TYPES)


def format_inr(amount: float) -> str:
    """Format rupees as Crores / Lakhs."""
    sign = "-" if amount < 0 else ""
    a = abs(amount)
    if a >= 1e7:
        return f"{sign}₹{a / 1e7:,.2f} Cr"
    if a >= 1e5:
        return f"{sign}₹{a / 1e5:,.2f} L"
    return f"{sign}₹{a:,.0f}"


@dataclass
class ValuationResult:
    total_budget: float
    capex_incurred: float
    remaining_budget: float
    finished_market_value: float
    current_asset_value: float
    steel_required_tonnes: float
    steel_consumed_tonnes: float
    cement_required_bags: int
    cement_consumed_bags: int
    cost_per_sqft: float
    current_milestone: str
    equity_gain: float


def current_milestone(completion_pct: float) -> str:
    for _lo, hi, name in MILESTONES:
        if completion_pct < hi:
            return name
    return MILESTONES[-1][2]


def compute_valuation(structure: str, sqft: float, tier: str, completion_pct: float) -> ValuationResult:
    if sqft <= 0:
        raise ValueError("Built-up area must be positive")
    if not 0 <= completion_pct <= 100:
        raise ValueError("Completion must be between 0 and 100")
    s, t = STRUCTURE_TYPES[structure], LOCATION_TIERS[tier]
    frac = completion_pct / 100

    cost_psf = s["cost_psf"] * t["cost_mult"] * (1 + CONTINGENCY_PCT)
    total_budget = cost_psf * sqft
    capex = total_budget * frac

    finished_value = s["market_psf"] * t["market_mult"] * sqft
    current_value = finished_value * (LAND_VALUE_SHARE + (1 - LAND_VALUE_SHARE) * frac)

    steel_total = s["steel_kg_psf"] * sqft / 1000
    cement_total = round(s["cement_bags_psf"] * sqft)

    return ValuationResult(
        total_budget=total_budget, capex_incurred=capex, remaining_budget=total_budget - capex,
        finished_market_value=finished_value, current_asset_value=current_value,
        steel_required_tonnes=steel_total, steel_consumed_tonnes=steel_total * frac,
        cement_required_bags=cement_total, cement_consumed_bags=round(cement_total * frac),
        cost_per_sqft=cost_psf, current_milestone=current_milestone(completion_pct),
        equity_gain=current_value - capex,
    )


def render_prompt(structure: str, tier: str, completion_pct: int, sqft: int) -> str:
    city = tier.split("(")[-1].rstrip(")").split(",")[0]
    return (f"Photorealistic architectural rendering of a {structure.lower()} in {city}, India, "
            f"about {sqft} sq ft, {completion_pct}% constructed, modern Indian architecture, "
            f"golden hour lighting, detailed concrete and glass facade, 3D visualization, ultra detailed")
