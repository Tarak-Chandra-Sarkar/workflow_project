from fastapi import FastAPI
from fastapi.responses import JSONResponse
from orchestrator.pipeline import run_pipeline
from pathlib import Path
import json

app = FastAPI(
    title="Multi-Agent Pipeline API",
    description="Trigger the multi-agent data pipeline and get auto-saved output",
    version="1.0.0"
)

@app.get("/run", summary="Run pipeline", response_description="Pipeline result with saved path")
def run_pipeline_endpoint():
    """
    Runs the async multi-agent pipeline and returns the results.
    Output is automatically saved in the `outputs/` directory.
    """
    try:
        # Run pipeline (async + auto-save)
        result = run_pipeline()

        # Find the latest output file in outputs/
        output_dir = Path("outputs")
        files = sorted(output_dir.glob("*.json"), reverse=True)
        latest_file = str(files[0]) if files else None

        # Return JSON with pipeline result + path to saved file
        response = {
            "status": "success",
            "saved_file": latest_file,
            "result": result
        }
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )