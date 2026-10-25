"""Weather-aware site protocols."""

WEATHER_PROTOCOLS = {
    "Normal": {
        "icon": "🌤️", "level": "Low",
        "headline": "Normal working conditions",
        "alerts": [
            {"title": "Routine controls", "severity": "Low",
             "actions": ["Morning toolbox talk and PPE check", "Inspect scaffolds, ladders and lifting tackle",
                         "Maintain housekeeping and access routes"]},
        ],
    },
    "High Wind": {
        "icon": "💨", "level": "Critical",
        "headline": "High wind: suspend elevated and lifting operations",
        "alerts": [
            {"title": "Crane & hoist operations", "severity": "Critical",
             "actions": ["Suspend crane lifts when wind exceeds the manufacturer limit (typically ~36-40 km/h sustained)",
                         "Lower booms, slew to weathervane, and lock the crane",
                         "Stop hoisting of sheets, formwork panels and large-area materials"]},
            {"title": "Work at height", "severity": "High",
             "actions": ["Stop work on scaffolds, roofs and slab edges", "Secure loose materials, formwork and tarpaulins",
                         "Check scaffold ties and bracing (IS 4014)"]},
            {"title": "Fresh concrete", "severity": "Medium",
             "actions": ["Protect fresh concrete from rapid drying with windbreaks and curing covers"]},
        ],
    },
    "Heavy Rain": {
        "icon": "🌧️", "level": "High",
        "headline": "Heavy rain: electrical, excavation and concrete controls",
        "alerts": [
            {"title": "Electrical hazard mitigation", "severity": "Critical",
             "actions": ["De-energise temporary supply in flooded areas", "Verify ELCB/RCCB trip tests; use IP-rated connectors",
                         "Keep cables off the ground; no wet-hand tool use"]},
            {"title": "Excavation & slopes", "severity": "High",
             "actions": ["Inspect trench shoring and slopes before re-entry (IS 3764)", "Pump out water; keep spoil 1 m+ from edges"]},
            {"title": "Concrete curing protocol", "severity": "Medium",
             "actions": ["Cover fresh pours with tarpaulin; avoid placing concrete in active rain",
                         "Re-check slump and water-cement ratio after rain on aggregates",
                         "Protect cement bags on pallets under cover"]},
        ],
    },
    "Extreme Heat": {
        "icon": "🔥", "level": "High",
        "headline": "Extreme heat: worker welfare and hot-weather concreting",
        "alerts": [
            {"title": "Heat stress control", "severity": "High",
             "actions": ["Shift heavy work to early morning/evening", "Provide shade, ORS and water every 20-30 minutes",
                         "Enforce rest breaks and watch for heat exhaustion symptoms"]},
            {"title": "Hot-weather concreting (IS 456 cl. 14.2)", "severity": "High",
             "actions": ["Keep concrete temperature below 40 °C at placement; use chilled water or ice and shaded aggregates",
                         "Pour at night or early morning; consider retarding admixtures",
                         "Begin curing immediately and keep surfaces continuously wet for 10 days"]},
            {"title": "Equipment", "severity": "Medium",
             "actions": ["Monitor engine/hydraulic temperatures", "Avoid leaving cylinders and fuel in direct sun"]},
        ],
    },
}
