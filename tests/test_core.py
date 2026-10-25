import pytest
from core.config import LOCATION_TIERS, STRUCTURE_TYPES
from core.demo_data import DEMO_CRACK, DEMO_SAFETY
from core.schemas import normalize_crack_report, normalize_safety_report, parse_json_text
from core.valuation import compute_valuation, format_inr

TIER2 = list(LOCATION_TIERS)[1]
APT = "Residential Apartment"


def test_format_inr():
    assert format_inr(2_50_00_000) == "₹2.50 Cr"
    assert format_inr(7_50_000) == "₹7.50 L"
    assert format_inr(5000) == "₹5,000"


def test_valuation_zero_and_full():
    z = compute_valuation(APT, 1000, TIER2, 0)
    assert z.capex_incurred == 0
    f = compute_valuation(APT, 1000, TIER2, 100)
    assert f.capex_incurred == pytest.approx(f.total_budget)
    assert f.current_asset_value == pytest.approx(f.finished_market_value)
    assert f.current_milestone == "Testing & handover"


def test_valuation_tier_ordering():
    t1, t2, t3 = (compute_valuation(APT, 1000, t, 50).total_budget for t in LOCATION_TIERS)
    assert t1 > t2 > t3


def test_valuation_invalid():
    with pytest.raises(ValueError):
        compute_valuation(APT, 0, TIER2, 10)
    with pytest.raises(ValueError):
        compute_valuation(APT, 100, TIER2, 120)


def test_parse_json_with_fences():
    assert parse_json_text('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json_text('Here: {"a": 2} done') == {"a": 2}
    with pytest.raises(ValueError):
        parse_json_text("no json")


def test_safety_normalisation_defaults():
    r = normalize_safety_report({"safety_score": 250, "hazards": [{"hazard": "x", "severity": "bogus"}]})
    assert r["safety_score"] == 100
    assert len(r["ppe_detection"]) == 4
    assert r["hazards"][0]["severity"] == "Medium"


def test_demo_payloads_valid():
    assert normalize_safety_report(DEMO_SAFETY)["overall_status"] == "Needs Improvement"
    assert normalize_crack_report(DEMO_CRACK)["defect_type"] == "Settlement"


def test_crack_normalisation_bad_values():
    r = normalize_crack_report({"defect_type": "weird", "crack_width_mm": "abc", "recommended_repairs": ["Epoxy"]})
    assert r["defect_type"] == "Hairline" and r["crack_width_mm"] == 0.0
    assert r["recommended_repairs"][0]["method"] == "Epoxy"
