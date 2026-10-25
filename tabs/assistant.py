"""Tab 4 - Daily Site Assistant & Weather-Aware Advisory."""
import streamlit as st

from core.gemini_client import GeminiService
from core.prompts import CHAT_SYSTEM
from core.weather import WEATHER_PROTOCOLS
from ui.components import bullet_list, info_card, pill

GREETING = "Hi, I'm SiteMate 👷. Ask me about concrete, steel, curing, safety, schedules or costs."


def render(service: GeminiService) -> None:
    st.subheader("🌦️ Daily Site Assistant & Weather Advisory")
    weather = st.radio("Today's site weather", list(WEATHER_PROTOCOLS), horizontal=True, key="weather_sel")
    proto = WEATHER_PROTOCOLS[weather]

    st.markdown(f"### {proto['icon']} {proto['headline']}  {pill(proto['level'], proto['level'])}",
                unsafe_allow_html=True)
    cols = st.columns(len(proto["alerts"]))
    for col, alert in zip(cols, proto["alerts"]):
        with col:
            info_card(f"{alert['title']} {pill(alert['severity'], alert['severity'])}", bullet_list(alert["actions"]))

    st.markdown("#### 💬 Site engineering assistant")
    if "chat" not in st.session_state:
        st.session_state["chat"] = [{"role": "assistant", "content": GREETING}]

    for m in st.session_state["chat"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask a construction question...", key="chat_in")
    if prompt:
        history = st.session_state["chat"][1:]  # skip static greeting
        st.session_state["chat"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply, err = service.chat(history, prompt, CHAT_SYSTEM.format(weather=weather))
            st.markdown(reply)
            if err:
                st.caption(f"⚠️ Live call failed ({err}); showing fallback answer.")
        st.session_state["chat"].append({"role": "assistant", "content": reply})

    if st.button("Clear conversation", key="chat_clear"):
        st.session_state["chat"] = [{"role": "assistant", "content": GREETING}]
        st.rerun()
