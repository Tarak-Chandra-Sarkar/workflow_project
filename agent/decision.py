'''
lightweight agent layer
'''

def agent_decision(data):
    """
    Simulated agent logic (replace with LLM later)
    """

    has_missing = any(row["age"] == 0 for row in data)
    multiple_countries = len(set(row["country"] for row in data)) > 1

    return {
        "use_advanced_clean": has_missing,
        "transform_mode": "advanced" if multiple_countries else "basic",
        "report_style": "executive" if len(data) > 2 else "summary",
    }