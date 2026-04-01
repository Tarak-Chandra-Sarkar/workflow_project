import streamlit as st
import requests
from pathlib import Path
import json
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Pipeline Dashboard", layout="wide")
st.title("🚀 Multi-Agent Pipeline Dashboard")

# FastAPI server URL
API_URL = "http://127.0.0.1:8000/run"

# Ensure outputs folder exists
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# ---------------- Sidebar ----------------
st.sidebar.header("Controls")

# Run pipeline button
if st.sidebar.button("Run Pipeline"):
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

# Select previous pipeline run
output_files = sorted(output_dir.glob("*.json"), reverse=True)
if "latest_file" in st.session_state:
    selected_file = st.session_state["latest_file"]
else:
    selected_file = output_files[0].name if output_files else None

selected_file = st.sidebar.selectbox(
    "Select Pipeline Run",
    [f.name for f in output_files],
    index=0
) if output_files else None

if not selected_file:
    st.warning("No pipeline outputs found. Run the pipeline first!")
    st.stop()

# ---------------- Load Data ----------------
selected_path = output_dir / selected_file
with open(selected_path, "r", encoding="utf-8") as f:
    data = json.load(f)

st.subheader(f"Pipeline Run: {selected_file}")

# ---------------- Summary Metrics ----------------
st.markdown("### 📊 Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(data["data"]))
col2.metric("Countries", len(set(row["country"] for row in data["data"])))
col3.metric("History Entries", len(data["history"]))
col4.metric("Report Type", data["report"].get("type","N/A") if isinstance(data["report"], dict) else "Custom")

# ---------------- Agent Decisions ----------------
st.markdown("### 🤖 Agent Decisions")
for record in data["history"]:
    timestamp = datetime.fromtimestamp(record["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    with st.expander(f"{record['agent']} @ {timestamp}"):
        st.json(record["decision"])
        st.info(f"Fallback Used: {record['fallback_used']}")

# ---------------- Final Data ----------------
st.markdown("### 🗂️ Final Data")
df = pd.DataFrame(data["data"])
st.dataframe(df)

# Optional quick charts
st.markdown("### 📈 Quick Insights")
cols = st.columns(2)
if "age" in df.columns:
    cols[0].bar_chart(df["age"])
if "country" in df.columns:
    cols[1].bar_chart(df["country"].value_counts())

# ---------------- Final Report ----------------
st.markdown("### 📑 Final Report")
if "message" in data["report"]:
    st.info(data["report"]["message"])