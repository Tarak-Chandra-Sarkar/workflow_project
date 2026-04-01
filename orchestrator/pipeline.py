from processes.fetch import fetch_data
from processes.clean import basic_clean, advanced_clean
from processes.transform import transform_basic, transform_advanced
from processes.report import generate_report

from agents.cleaning_agent import CleaningAgent
from agents.transformation_agent import TransformationAgent
from agents.reporting_agent import ReportingAgent

from utils import log_step


def run_pipeline():
    # Initialize agents
    cleaning_agent = CleaningAgent("CleaningAgent")
    transform_agent = TransformationAgent("TransformationAgent")
    report_agent = ReportingAgent("ReportingAgent")

    # Step 1: Fetch
    data = fetch_data()
    log_step("Fetched Data", data)

    # Step 2: Basic Clean
    data = basic_clean(data)
    log_step("After Basic Clean", data)

    # Step 3: Cleaning Agent Decision
    clean_decision = cleaning_agent.decide(data)

    if clean_decision["use_advanced_clean"]:
        data = advanced_clean(data)
        log_step("After Advanced Clean", data)

    # Step 4: Transformation Agent Decision
    transform_decision = transform_agent.decide(data)

    if transform_decision["mode"] == "advanced":
        data = transform_advanced(data)
    else:
        data = transform_basic(data)

    log_step("After Transformation", data)

    # Step 5: Reporting Agent Decision
    report_decision = report_agent.decide(data)

    report = generate_report(data, style=report_decision["style"])
    log_step("Final Report", report)

    return {
        "data": data,
        "report": report,
        "decisions": {
            "cleaning": clean_decision,
            "transformation": transform_decision,
            "reporting": report_decision
        }
    }