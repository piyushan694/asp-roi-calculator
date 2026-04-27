# Alexa+ ROI Analysis — Partner Calculator

Interactive ROI dashboard for modeling Alexa+ for Hospitality deployment impact on partner revenue and profitability.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run roi_calculator.py
```

Opens at http://localhost:8501

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repo (public or private if you have a paid plan)
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click **New app** → pick the repo → set main file to `roi_calculator.py`
5. Click **Deploy** — you'll get a permanent URL like `https://<name>.streamlit.app`

## Structure

- `roi_calculator.py` — main app (4 tabs: Executive Summary, Live Scenario Builder, Calculation Walkthrough, Sensitivity Analysis)
- `assets/` — drop the Alexa+ brand logo here as `alexa-plus-logo.png` to render it in the hero
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — theme defaults
- `share.py` — optional local ngrok tunneling launcher

## Confidentiality

This app models partner-specific deal terms. If deploying publicly on Streamlit Cloud, consider:
- Adding basic password protection via `st.secrets`
- Clearing partner-specific defaults before deploy
- Using a private GitHub repo + Streamlit Cloud paid tier
