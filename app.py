"""Multimodal Construction Intelligence Platform - Streamlit entry point."""
import os
import streamlit as st

from core.config import APP_NAME, APP_TAGLINE, DEFAULT_MODEL, MODEL_OPTIONS
from core.gemini_client import GeminiService
from tabs import assistant, cracks, planning, safety
from ui.styles import inject_css

st.set_page_config(page_title=APP_NAME, page_icon="🏗️", layout="wide")
inject_css()


def _secret_key() -> str:
    """Server-side key from Streamlit secrets or environment (never sent to the browser)."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "")


def sidebar() -> GeminiService:
    with st.sidebar:
        st.markdown("## 🏗️ Control Panel")
        server_key = _secret_key()
        typed = st.text_input(
            "Google Gemini API key",
            type="password",
            placeholder="Using app key; paste yours to override" if server_key else "Paste key (blank = demo mode)",
            help="Never stored. Leave blank to use the app default or demonstration mode.",
        )
        key = typed.strip() or server_key
        model = st.selectbox("Model", MODEL_OPTIONS, index=MODEL_OPTIONS.index(DEFAULT_MODEL))
        service = GeminiService(key, model)
        if service.demo_mode:
            st.warning("Demonstration mode: sample outputs are shown.")
        else:
            st.success("Live Gemini connected." + (" (app key)" if not typed.strip() else " (your key)"))
        st.divider()
        st.markdown("### Features")
        st.markdown(
            "- 🦺 Site Safety & PPE Audit\n- 🧱 Crack Diagnostics\n"
            "- 📐 Planning & Valuation\n- 🌦️ Weather & Site Assistant"
        )
        with st.expander("Architecture overview"):
            st.markdown(
                "**Streamlit UI** → `tabs/*` modules\n\n"
                "**Core services**\n- `gemini_client` multimodal calls + demo fallback\n"
                "- `schemas` JSON data contracts\n- `valuation` INR cost engine\n- `weather` protocols\n\n"
                "**External**: Gemini API, Pollinations (Flux) image API. No database."
            )
        st.caption("Get a free key at aistudio.google.com")
    return service


def main() -> None:
    service = sidebar()
    st.markdown(
        f'<div class="hero"><h1>🏗️ {APP_NAME}</h1>'
        f"<p>{APP_TAGLINE} · Safety · Structural · Cost · Weather intelligence</p></div>",
        unsafe_allow_html=True,
    )
    t1, t2, t3, t4 = st.tabs(
        ["🦺 Safety & PPE", "🧱 Crack Diagnostics", "📐 Planning & Valuation", "🌦️ Site Assistant"]
    )
    with t1:
        safety.render(service)
    with t2:
        cracks.render(service)
    with t3:
        planning.render()
    with t4:
        assistant.render(service)


main()