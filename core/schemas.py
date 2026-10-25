"""JSON data contracts: normalise and validate model output so the UI never breaks."""
from __future__ import annotations
import json
import re
from typing import Any

from core.config import (DEFECT_TYPES, OVERALL_STATUSES, PPE_ITEMS, SEVERITY_LEVELS, URGENCY_LEVELS)


def parse_json_text(text: str) -> dict:
    """Extract a JSON object from raw LLM text (handles ```json fences / stray prose)."""
    if not text:
        raise ValueError("Empty model response")
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in model response")
        return json.loads(match.group(0))


def _clamp_int(value: Any, lo: int, hi: int, default: int = 0) -> int:
    try:
        return max(lo, min(hi, int(round(float(value)))))
    except (TypeError, ValueError):
        return default


def _pick(value: Any, allowed: list, default: str) -> str:
    if isinstance(value, str):
        for opt in allowed:
            if value.strip().lower() == opt.lower():
                return opt
    return default


def normalize_safety_report(data: dict) -> dict:
    score = _clamp_int(data.get("safety_score"), 0, 100)
    ppe_raw = {str(p.get("item", "")).lower(): p for p in data.get("ppe_detection", []) if isinstance(p, dict)}
    ppe = []
    for item in PPE_ITEMS:
        p = ppe_raw.get(item.lower(), {})
        ppe.append({
            "item": item,
            "status": _pick(p.get("status"), ["Detected", "Missing", "Not Visible"], "Not Visible"),
            "compliance_pct": _clamp_int(p.get("compliance_pct"), 0, 100),
            "notes": str(p.get("notes", "")),
        })
    hazards = []
    for h in data.get("hazards", []) or []:
        if isinstance(h, dict) and h.get("hazard"):
            hazards.append({
                "hazard": str(h["hazard"]),
                "severity": _pick(h.get("severity"), SEVERITY_LEVELS, "Medium"),
                "location": str(h.get("location", "Not specified")),
                "remedy": str(h.get("remedy", "Consult site safety officer")),
                "standard_reference": str(h.get("standard_reference", "")),
            })
    return {
        "safety_score": score,
        "overall_status": _pick(data.get("overall_status"), OVERALL_STATUSES,
                                "Compliant" if score >= 85 else "Needs Improvement" if score >= 60 else "Non-Compliant"),
        "workers_detected": _clamp_int(data.get("workers_detected"), 0, 10000),
        "summary": str(data.get("summary", "")),
        "ppe_detection": ppe,
        "hazards": hazards,
    }


def normalize_crack_report(data: dict) -> dict:
    try:
        width = round(max(0.0, float(data.get("crack_width_mm", 0))), 2)
    except (TypeError, ValueError):
        width = 0.0
    repairs = []
    for r in data.get("recommended_repairs", []) or []:
        if isinstance(r, dict):
            repairs.append({"method": str(r.get("method", "Engineer review")), "details": str(r.get("details", ""))})
        elif isinstance(r, str):
            repairs.append({"method": r, "details": ""})
    return {
        "defect_type": _pick(data.get("defect_type"), DEFECT_TYPES, "Hairline"),
        "crack_width_mm": width,
        "severity_score": _clamp_int(data.get("severity_score"), 0, 100),
        "urgency": _pick(data.get("urgency"), URGENCY_LEVELS, "Monitor"),
        "structural_risk": _pick(data.get("structural_risk"), SEVERITY_LEVELS, "Low"),
        "confidence_pct": _clamp_int(data.get("confidence_pct"), 0, 100),
        "summary": str(data.get("summary", "")),
        "root_causes": [str(c) for c in data.get("root_causes", []) or []],
        "recommended_repairs": repairs,
        "monitoring_plan": str(data.get("monitoring_plan", "")),
    }
