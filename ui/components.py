"""Reusable UI building blocks."""
import html
import streamlit as st


def metric_card(label: str, value: str, sub: str = "") -> str:
    return (f'<div class="metric-card"><div class="label">{html.escape(label)}</div>'
            f'<div class="value">{html.escape(value)}</div><div class="sub">{html.escape(sub)}</div></div>')


def show_metrics(items: list) -> None:
    """items: list of (label, value, sub)."""
    cols = st.columns(len(items))
    for col, (label, value, sub) in zip(cols, items):
        col.markdown(metric_card(label, value, sub), unsafe_allow_html=True)


def pill(text: str, level: str = "info") -> str:
    return f'<span class="pill pill-{level.lower()}">{html.escape(text)}</span>'


def level_for_score(score: int) -> str:
    """Higher score = safer."""
    return "low" if score >= 85 else "medium" if score >= 60 else "high" if score >= 40 else "critical"


def source_banner(source: str, error: str = None) -> None:
    if source == "demo":
        msg = "🧪 <b>Demonstration mode</b> — showing a sample result. Add a Gemini API key in the sidebar for live analysis."
        if error:
            msg += f"<br><small>Live call failed, showing demo data instead: {html.escape(error)}</small>"
        st.markdown(f'<div class="banner-demo">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="banner-live">✅ <b>Live analysis</b> by Gemini multimodal model.</div>',
                    unsafe_allow_html=True)


def info_card(title: str, body_html: str) -> None:
    st.markdown(f'<div class="card"><h4>{title}</h4>{body_html}</div>', unsafe_allow_html=True)


def bullet_list(items: list) -> str:
    return "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"
