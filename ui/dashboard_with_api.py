import streamlit as st
import requests
from pathlib import Path
import json
from datetime import datetime
import time

st.set_page_config(page_title="Multi-Agent Pipeline Dashboard", layout="wide")

st.title("🚀 Multi-Agent Pipeline Dashboard with Trigger")

# FastAPI server URL (adjust if running remotely)
API_URL = "http://127.0.0.1:8000/run"

# Outputs folder
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

st.sidebar.header("Pipeline Controls")

# Trigger pipeline button
if st.sidebar.button("Run Pipeline"):
    with st.spinner("Running pipeline..."):
        try:
            response = requests.get(API_URL, timeout=120)  # call FastAPI endpoint
            if response.status_code == 200:
                st.success("Pipeline completed successfully!")
                result = response.json()
                st.session_state["latest_file"] = result["saved_file"]
            else:
                st.error(f"Pipeline failed: {response.text}")
        except Exception as e:
            st.error(f"Error calling pipeline API: {e}")

# Select pipeline run
st.sidebar.markdown("### Select Pipeline Run")
output_files = sorted(output_dir.glob("*.json"), reverse=True)
if "latest_file" in st.session_state:
    selected_file = st.session_state["latest_file"]
else:
    selected_file = output_files[0].name if output_files else None

selected_file = st.sidebar.selectbox(
    "Choose output JSON", [f.name for f in output_files], index=0
) if output_files else None

if not selected_file:
    st.warning("No pipeline outputs found. Run the pipeline first!")
    st.stop()

selected_path = output_dir / selected_file

# Load JSON data
with open(selected_path, "r", encoding="utf-8") as f:
    data = json.load(f)

st.subheader(f"Pipeline Run: {selected_file}")

# Display summary metrics
st.markdown("### ✅ Summary")
st.write({
    "Total Records": len(data["data"]),
    "Report Type": data["report"].get("type", "N/A") if isinstance(data["report"], dict) else "Custom",
    "History Length": len(data["history"])
})

# Display agent decisions
st.markdown("### 🤖 Agent Decisions")
for record in data["history"]:
    timestamp = datetime.fromtimestamp(record["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"**{record['agent']}** at {timestamp}")
    st.json(record["decision"])
    st.write(f"Fallback Used: {record['fallback_used']}")

# Show final data table
st.markdown("### 🗂️ Final Data")
st.dataframe(data["data"])

# Show final report
st.markdown("### 📊 Final Report")
st.markdown(f"**Executive Message:** {data['report'].get('message','')}")
st.json(data["report"])