# dashboard_with_api.py
import streamlit as st
import requests
from pathlib import Path
import json
from datetime import datetime
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ---------------- Page Config ----------------
st.set_page_config(page_title="Pipeline Dashboard", layout="wide")
st.title("🚀 Multi-Agent Pipeline Dashboard")

# ---------------- Config ----------------
API_URL = "http://127.0.0.1:8000/run"
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)
AUTO_REFRESH_INTERVAL = 5  # seconds

# ---------------- Sidebar Controls ----------------
st.sidebar.header("Controls")

# Style native Streamlit button
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        font-weight: bold;
        padding: 12px 0px;
        border-radius: 8px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #45A049;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state to track click
if "run_pipeline_click" not in st.session_state:
    st.session_state.run_pipeline_click = False

# Native Streamlit button (styled via CSS)
if st.sidebar.button("🚀 Run Pipeline"):
    st.session_state.run_pipeline_click = True

# ---------------- Run Pipeline ----------------
if st.session_state.run_pipeline_click:
    with st.spinner("Running pipeline..."):
        try:
            response = requests.get(API_URL, timeout=120)
            if response.status_code == 200:
                st.success("Pipeline completed successfully!")
                result = response.json()
                st.session_state["latest_file"] = result["saved_file"]
            else:
                st.error(f"Pipeline failed: {response.text}")
        except Exception as e:
            st.error(f"Error calling pipeline API: {e}")
    st.session_state.run_pipeline_click = False

# ---------------- Select Output JSON ----------------
output_files = sorted(OUTPUT_DIR.glob("*.json"), reverse=True)
if "latest_file" in st.session_state:
    selected_file = st.session_state["latest_file"]
else:
    selected_file = output_files[0].name if output_files else None

if not selected_file:
    st.warning("No pipeline outputs found. Run the pipeline first!")
    st.stop()

selected_file = st.sidebar.selectbox(
    "Select Pipeline Run",
    [f.name for f in output_files],
    index=0
) if output_files else None

selected_path = OUTPUT_DIR / selected_file

# ---------------- Live Auto-Refresh ----------------
count = st_autorefresh(interval=AUTO_REFRESH_INTERVAL * 1000, key="pipeline_refresh")

# ---------------- Load Data ----------------
with open(selected_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------------- Tabs ----------------
tabs = st.tabs(["📊 Data", "🤖 Agents", "📑 Report"])

# ---------------- Tab 1: Data ----------------
with tabs[0]:
    st.subheader("🗂️ Data Preview")
    df = pd.DataFrame(data["data"])

    # Filter by Country
    if "country" in df.columns:
        countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
        selected_country = st.selectbox("Filter by Country", countries)
        if selected_country != "All":
            df = df[df["country"] == selected_country]

    st.dataframe(df)

    # Quick Charts
    st.markdown("### Charts")
    cols = st.columns(2)
    if "age" in df.columns:
        cols[0].bar_chart(df["age"])
    if "country" in df.columns:
        cols[1].bar_chart(df["country"].value_counts())

# ---------------- Tab 2: Agents ----------------
with tabs[1]:
    st.subheader("🤖 Agent Decisions")
    agents_list = sorted(list({record["agent"] for record in data["history"]}))
    agents_list = ["All"] + agents_list
    selected_agent = st.selectbox("Filter by Agent", agents_list)

    for record in data["history"]:
        if selected_agent != "All" and record["agent"] != selected_agent:
            continue

        timestamp = datetime.fromtimestamp(record["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        with st.expander(f"{record['agent']} @ {timestamp}"):
            st.json(record["decision"])
            fallback = record["fallback_used"]
            # Colored badge
            badge_color = "#4CAF50" if not fallback else "#FF4136"
            badge_text = "Fallback Used" if fallback else "No Fallback"
            st.markdown(
                f'<span style="background-color:{badge_color};color:white;padding:4px 8px;border-radius:4px;">{badge_text}</span>',
                unsafe_allow_html=True
            )

# ---------------- Tab 3: Report ----------------
with tabs[2]:
    st.subheader("📑 Final Report")
    if isinstance(data["report"], dict) and "message" in data["report"]:
        st.info(data["report"]["message"])
    st.json(data["report"])