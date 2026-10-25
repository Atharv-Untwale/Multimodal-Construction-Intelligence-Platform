"""Tab 2 - Crack Diagnostics & Structural Integrity."""
import html
import json
import streamlit as st

from core.config import ALLOWED_IMAGE_TYPES, DEFECT_TYPES, DISCLAIMER
from core.demo_data import DEMO_CRACK
from core.gemini_client import GeminiService, prepare_image
from core.prompts import CRACK_PROMPT
from core.schemas import normalize_crack_report
from ui.components import bullet_list, info_card, pill, show_metrics, source_banner

URGENCY_LEVEL = {"Monitor": "low", "Within 30 Days": "medium", "Within 7 Days": "high", "Immediate": "critical"}
DEFECT_HINT = {
    "Hairline": "Surface shrinkage cracks, typically < 0.3 mm; mostly cosmetic.",
    "Settlement": "Diagonal/stepped cracks from differential foundation movement.",
    "Structural Shear": "45° cracks near supports or beam-column joints; load-bearing concern.",
    "Thermal Expansion": "Regular-interval cracks from temperature cycles; check joints.",
    "Spalling": "Concrete surface flaking, often from rebar corrosion.",
}


def render(service: GeminiService) -> None:
    st.subheader("🧱 Crack Diagnostics & Structural Integrity")
    st.caption("Classify defects, estimate crack width and get engineering repair guidance (IS 456 / IS 15988).")
    file = st.file_uploader("Concrete / wall surface photo", type=ALLOWED_IMAGE_TYPES, key="crack_up")

    if file is not None:
        try:
            image = prepare_image(file)
        except Exception as exc:
            st.error(f"Could not read the image: {exc}")
            return
        st.image(image, caption="Uploaded surface", width=420)
        if st.button("🔬 Diagnose defect", type="primary", key="crack_run"):
            with st.spinner("Diagnosing structural defect..."):
                st.session_state["crack_report"] = service.analyze_image(
                    CRACK_PROMPT, image, normalize_crack_report, DEMO_CRACK)
    else:
        st.info("Upload a JPG/PNG photo to begin, or preview a sample report.")
        if st.button("Preview sample report", key="crack_demo"):
            st.session_state["crack_report"] = (normalize_crack_report(DEMO_CRACK), "demo", None)

    with st.expander("Defect type reference"):
        for d in DEFECT_TYPES:
            st.markdown(f"**{d}** — {DEFECT_HINT[d]}")

    if "crack_report" in st.session_state:
        report, source, err = st.session_state["crack_report"]
        _show_report(report, source, err)


def _show_report(r: dict, source: str, err) -> None:
    source_banner(source, err)
    show_metrics([
        ("Defect type", r["defect_type"], f'Confidence {r["confidence_pct"]}%'),
        ("Crack width", f'{r["crack_width_mm"]} mm', "Estimated"),
        ("Severity score", f'{r["severity_score"]}/100', "Higher is worse"),
        ("Urgency", r["urgency"], f'Risk: {r["structural_risk"]}'),
    ])
    st.progress(r["severity_score"] / 100)
    st.markdown(pill(f'Risk: {r["structural_risk"]}', r["structural_risk"]) + "  " +
                pill(r["urgency"], URGENCY_LEVEL[r["urgency"]]), unsafe_allow_html=True)
    if r["summary"]:
        st.write(r["summary"])

    c1, c2 = st.columns(2)
    with c1:
        info_card("🔎 Probable root causes", bullet_list(r["root_causes"]) if r["root_causes"] else "—")
    with c2:
        repairs = "".join(f"<li><b>{html.escape(x['method'])}</b>: {html.escape(x['details'])}</li>"
                          for x in r["recommended_repairs"])
        info_card("🛠️ Recommended repairs", f"<ul>{repairs}</ul>" if repairs else "—")
    if r["monitoring_plan"]:
        info_card("📈 Monitoring plan", f'<div style="color:#CBD5E1">{html.escape(r["monitoring_plan"])}</div>')

    st.download_button("⬇️ Download JSON report", json.dumps(r, indent=2, ensure_ascii=False),
                       file_name="crack_diagnostic_report.json", mime="application/json", key="crack_dl")
    st.markdown(f'<div class="disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)
