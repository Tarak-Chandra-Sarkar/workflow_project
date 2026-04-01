from orchestrator.pipeline import run_pipeline

if __name__ == "__main__":
    result = run_pipeline()

    print("\n=== FINAL OUTPUT ===")
    print(result)