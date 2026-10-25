# 🏗️ Multimodal Construction Intelligence Platform
Skill Wallet Capstone – Project 1 (Streamlit + Gemini)

Analyse site photos for PPE compliance, classify concrete cracks, estimate budget and valuation in INR,
and get weather-aware protocols plus a construction chatbot. No database; runs in demo mode without a key.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
pytest -q            # run tests
```
Add a Gemini key in the sidebar, or set `GEMINI_API_KEY` (env var or `.streamlit/secrets.toml`).

## Deploy (Streamlit Community Cloud)
1. Push this folder to GitHub.  2. New app → select repo, main file `app.py`.
3. App settings → Secrets → `GEMINI_API_KEY = "..."` (optional).

## Structure
```
app.py                 entry point, sidebar, tabs
core/config.py         constants, rates, enums      core/schemas.py   JSON contracts
core/prompts.py        multimodal prompts           core/valuation.py INR engine
core/gemini_client.py  Gemini + demo fallback       core/weather.py   protocols
core/demo_data.py      sample outputs               ui/               CSS + components
tabs/                  safety, cracks, planning, assistant
tests/test_core.py     unit tests
```
## Epic mapping
E1 env/requirements · E2 `tabs/safety.py`, `tabs/cracks.py` · E3 `tabs/planning.py`, `core/valuation.py`
E4 `core/prompts.py`, `core/schemas.py` · E5 `tabs/assistant.py`, `core/weather.py` · E6 UI, tests, deploy

## Notes
- Default model is `gemini-2.5-flash` (selectable); update `MODEL_OPTIONS` in `core/config.py` as models change.
- Cost/market rates are indicative placeholders; tune them to local data.
- AI output is advisory and needs sign-off from a qualified engineer / safety officer.
