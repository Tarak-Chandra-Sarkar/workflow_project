from orchestrator.pipeline import run_pipeline

if __name__ == "__main__":
    # Run the pipeline (async + auto-save)
    result = run_pipeline()

    print("\n=== FINAL OUTPUT ===")
    print(result)