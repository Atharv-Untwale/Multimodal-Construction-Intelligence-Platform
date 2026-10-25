"""Modern dark CSS theme."""
import streamlit as st

CSS = """
<style>
.block-container {padding-top: 1.6rem; max-width: 1200px;}
.hero {background: linear-gradient(135deg,#1E293B 0%,#0F172A 55%,#78350F 140%);
       border:1px solid #334155; border-radius:18px; padding:1.4rem 1.8rem; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:1.9rem; color:#F8FAFC;}
.hero p {margin:.3rem 0 0; color:#94A3B8;}
.metric-card {background:#1E293B; border:1px solid #334155; border-radius:14px; padding:1rem 1.1rem; height:100%;}
.metric-card .label {font-size:.75rem; letter-spacing:.06em; text-transform:uppercase; color:#94A3B8;}
.metric-card .value {font-size:1.7rem; font-weight:700; color:#F8FAFC; line-height:1.25;}
.metric-card .sub {font-size:.8rem; color:#64748B;}
.pill {display:inline-block; padding:.2rem .75rem; border-radius:999px; font-size:.78rem; font-weight:600; border:1px solid;}
.pill-low {background:#052E1B; color:#34D399; border-color:#065F46;}
.pill-medium {background:#3B2F05; color:#FBBF24; border-color:#92400E;}
.pill-high {background:#3B1D05; color:#FB923C; border-color:#9A3412;}
.pill-critical {background:#3B0A0A; color:#F87171; border-color:#991B1B;}
.pill-info {background:#0C2A44; color:#38BDF8; border-color:#075985;}
.card {background:#1E293B; border:1px solid #334155; border-radius:14px; padding:1rem 1.2rem; margin-bottom:.7rem;}
.card h4 {margin:0 0 .4rem; color:#F8FAFC; font-size:1rem;}
.card ul {margin:.3rem 0 0 1rem; padding:0; color:#CBD5E1;}
.banner-demo {background:#3B2F05; border:1px solid #92400E; color:#FDE68A; padding:.55rem .9rem;
              border-radius:10px; font-size:.85rem; margin-bottom:.8rem;}
.banner-live {background:#052E1B; border:1px solid #065F46; color:#6EE7B7; padding:.55rem .9rem;
              border-radius:10px; font-size:.85rem; margin-bottom:.8rem;}
.disclaimer {color:#64748B; font-size:.78rem; margin-top:.8rem;}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
