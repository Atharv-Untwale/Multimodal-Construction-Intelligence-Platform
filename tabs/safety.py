"""Tab 1 - Site Safety & PPE Audit."""
import html
import json
import streamlit as st

from core.config import ALLOWED_IMAGE_TYPES, DISCLAIMER, SEVERITY_LEVELS
from core.demo_data import DEMO_SAFETY
from core.gemini_client import GeminiService, prepare_image
from core.prompts import SAFETY_PROMPT
from core.schemas import normalize_safety_report
from ui.components import bullet_list, info_card, level_for_score, pill, show_metrics, source_banner

STATUS_LEVEL = {"Compliant": "low", "Needs Improvement": "medium", "Non-Compliant": "critical"}
PPE_ICON = {"Detected": "✅", "Missing": "❌", "Not Visible": "➖"}


def render(service: GeminiService) -> None:
    st.subheader("🦺 Site Safety & PPE Audit")
    st.caption("Upload a site photo to audit PPE compliance and identify hazards (OSHA 1926 / IS codes).")
    file = st.file_uploader("Construction site photo", type=ALLOWED_IMAGE_TYPES, key="safety_up")

    if file is not None:
        try:
            image = prepare_image(file)
        except Exception as exc:
            st.error(f"Could not read the image: {exc}")
            return
        st.image(image, caption="Uploaded site photo", width=420)
        if st.button("🔍 Run safety audit", type="primary", key="safety_run"):
            with st.spinner("Analysing site photo..."):
                st.session_state["safety_report"] = service.analyze_image(
                    SAFETY_PROMPT, image, normalize_safety_report, DEMO_SAFETY)
    else:
        st.info("Upload a JPG/PNG photo to begin, or preview a sample report.")
        if st.button("Preview sample report", key="safety_demo"):
            st.session_state["safety_report"] = (normalize_safety_report(DEMO_SAFETY), "demo", None)

    if "safety_report" in st.session_state:
        report, source, err = st.session_state["safety_report"]
        _show_report(report, source, err)


def _show_report(report: dict, source: str, err) -> None:
    source_banner(source, err)
    score, status = report["safety_score"], report["overall_status"]
    show_metrics([
        ("Safety score", f"{score}/100", "Higher is safer"),
        ("Overall status", status, "Site compliance"),
        ("Workers detected", str(report["workers_detected"]), "In frame"),
        ("Hazards found", str(len(report["hazards"])), f"{sum(h['severity'] == 'Critical' for h in report['hazards'])} critical"),
    ])
    st.progress(score / 100)
    st.markdown(pill(status, STATUS_LEVEL.get(status, "info")) + "  " +
                pill(f"Score {score}", level_for_score(score)), unsafe_allow_html=True)
    if report["summary"]:
        st.write(report["summary"])

    st.markdown("#### PPE checklist")
    cols = st.columns(len(report["ppe_detection"]))
    for col, p in zip(cols, report["ppe_detection"]):
        lvl = "low" if p["status"] == "Detected" and p["compliance_pct"] >= 80 else \
              "high" if p["status"] == "Missing" else "medium"
        col.markdown(
            f'<div class="card"><h4>{PPE_ICON[p["status"]]} {html.escape(p["item"])}</h4>'
            f'{pill(p["status"], lvl)}<div class="sub" style="margin-top:.5rem;color:#94A3B8">'
            f'{p["compliance_pct"]}% compliant<br>{html.escape(p["notes"])}</div></div>', unsafe_allow_html=True)

    st.markdown("#### Identified hazards")
    if not report["hazards"]:
        st.success("No hazards identified.")
    for sev in reversed(SEVERITY_LEVELS):
        for h in (x for x in report["hazards"] if x["severity"] == sev):
            info_card(
                f'{html.escape(h["hazard"])} &nbsp; {pill(h["severity"], h["severity"])}',
                f'<div style="color:#94A3B8">📍 {html.escape(h["location"])}</div>'
                f'<div style="margin-top:.3rem"><b>Remedy:</b> {html.escape(h["remedy"])}</div>'
                f'<div style="color:#64748B;font-size:.8rem">{html.escape(h["standard_reference"])}</div>')

    st.download_button("⬇️ Download JSON report", json.dumps(report, indent=2, ensure_ascii=False),
                       file_name="safety_audit_report.json", mime="application/json", key="safety_dl")
    st.markdown(f'<div class="disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)
