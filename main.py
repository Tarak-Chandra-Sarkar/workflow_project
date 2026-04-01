import json
import time
from pathlib import Path
from orchestrator.pipeline import run_pipeline

if __name__ == "__main__":
    # Run the pipeline
    result = run_pipeline()

    print("\n=== FINAL OUTPUT ===")
    print(result)

    # Ensure output directory exists
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    # Save JSON file with timestamp
    filename = output_dir / f"pipeline_output_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Output saved to {filename}")