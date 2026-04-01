'''
orchestrator
'''

from processes.fetch import fetch_data
from processes.clean import basic_clean, advanced_clean
from processes.transform import transform_basic, transform_advanced
from processes.report import generate_report

from agent.decision import agent_decision
from config import USE_AGENT
from utils import log_step


def run_pipeline():
    # Step 1: Fetch
    data = fetch_data()
    log_step("Fetched Data", data)

    # Step 2: Basic Clean
    data = basic_clean(data)
    log_step("After Basic Clean", data)

    # Step 3: Agent Decision
    if USE_AGENT:
        decision = agent_decision(data)
    else:
        decision = {
            "use_advanced_clean": False,
            "transform_mode": "basic",
            "report_style": "summary",
        }

    print("\nAgent Decision:", decision)

    # Step 4: Optional Advanced Clean
    if decision["use_advanced_clean"]:
        data = advanced_clean(data)
        log_step("After Advanced Clean", data)

    # Step 5: Transformation
    if decision["transform_mode"] == "advanced":
        data = transform_advanced(data)
    else:
        data = transform_basic(data)

    log_step("After Transformation", data)

    # Step 6: Report
    report = generate_report(data, style=decision["report_style"])
    log_step("Final Report", report)

    return report


if __name__ == "__main__":
    run_pipeline()