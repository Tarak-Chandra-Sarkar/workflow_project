import copy
import time

from processes.fetch import fetch_data
from processes.clean import basic_clean, advanced_clean
from processes.transform import transform_basic, transform_advanced
from processes.report import generate_report

from agents.cleaning_agent import CleaningAgent
from agents.transformation_agent import TransformationAgent
from agents.reporting_agent import ReportingAgent

from utils import log_step


def safe_decide(agent, data, default):
    try:
        return agent.decide(data)
    except Exception as e:
        agent.log(f"Error: {e}, using fallback")
        return default


def run_pipeline():
    # Initialize context
    context = {
        "data": fetch_data(),
        "history": []
    }

    # Initialize agents
    cleaning_agent = CleaningAgent("CleaningAgent")
    transform_agent = TransformationAgent("TransformationAgent")
    report_agent = ReportingAgent("ReportingAgent")

    # Step 1: Fetch
    log_step("Fetched Data", context["data"])

    # Step 2: Basic Clean
    context["data"] = basic_clean(copy.deepcopy(context["data"]))
    log_step("After Basic Clean", context["data"])

    # Step 3: Cleaning Decision
    clean_decision = safe_decide(
        cleaning_agent,
        context["data"],
        {"action": "basic_clean", "reason": "fallback", "confidence": 0.5}
    )

    context["history"].append({
    "agent": cleaning_agent.name,
    "decision": clean_decision,
    "fallback_used": clean_decision["reason"] == "fallback",
    "timestamp": time.time()
    })

    if clean_decision["action"] == "advanced_clean":
        context["data"] = advanced_clean(copy.deepcopy(context["data"]))
        log_step("After Advanced Clean", context["data"])

    # Step 4: Transformation Decision
    transform_decision = safe_decide(
        transform_agent,
        context["data"],
        {"action": "basic", "reason": "fallback", "confidence": 0.5}
    )

    context["history"].append({
    "agent": transform_agent.name,
    "decision": transform_decision,
    "fallback_used": transform_decision["reason"] == "fallback",
    "timestamp": time.time()
    })

    if transform_decision["action"] == "advanced":
        context["data"] = transform_advanced(copy.deepcopy(context["data"]))
    else:
        context["data"] = transform_basic(copy.deepcopy(context["data"]))

    log_step("After Transformation", context["data"])

    # Step 5: Reporting Decision
    report_decision = safe_decide(
        report_agent,
        context["data"],
        {"action": "summary", "reason": "fallback", "confidence": 0.5}
    )

    context["history"].append({
        "agent": report_agent.name,
        "decision": report_decision,
        "fallback_used": report_decision["reason"] == "fallback",
        "timestamp": time.time()
    })

    report = generate_report(
        context["data"],
        style=report_decision["action"]
    )

    log_step("Final Report", report)

    return {
        "data": context["data"],
        "report": report,
        "history": context["history"]
    }