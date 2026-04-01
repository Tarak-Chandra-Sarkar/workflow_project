import copy
import time
import asyncio
import json
from pathlib import Path

from processes.fetch import fetch_data
from processes.clean import basic_clean, advanced_clean
from processes.transform import transform_basic, transform_advanced
from processes.report import generate_report

from agents.cleaning_agent import CleaningAgent
from agents.transformation_agent import TransformationAgent
from agents.reporting_agent import ReportingAgent

from utils import log_step

# Safe decision function
def safe_decide(agent, data, default):
    try:
        return agent.decide(data)
    except Exception as e:
        agent.log(f"Error: {e}, using fallback")
        return default

# Async wrapper for agents
async def run_agent(agent, data, default):
    return safe_decide(agent, data, default)

# Async pipeline
async def run_pipeline_async(save_output=True):
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

    # Step 3: Run all agents concurrently
    clean_default = {"action": "basic_clean", "reason": "fallback", "confidence": 0.5}
    transform_default = {"action": "basic", "reason": "fallback", "confidence": 0.5}
    report_default = {"action": "summary", "reason": "fallback", "confidence": 0.5}

    clean_decision, transform_decision, report_decision = await asyncio.gather(
        run_agent(cleaning_agent, context["data"], clean_default),
        run_agent(transform_agent, context["data"], transform_default),
        run_agent(report_agent, context["data"], report_default),
    )

    # Record decisions in history
    timestamp = time.time()
    context["history"].append({
        "agent": cleaning_agent.name,
        "decision": clean_decision,
        "fallback_used": clean_decision["reason"] == "fallback",
        "timestamp": timestamp
    })
    context["history"].append({
        "agent": transform_agent.name,
        "decision": transform_decision,
        "fallback_used": transform_decision["reason"] == "fallback",
        "timestamp": timestamp
    })
    context["history"].append({
        "agent": report_agent.name,
        "decision": report_decision,
        "fallback_used": report_decision["reason"] == "fallback",
        "timestamp": timestamp
    })

    # Step 4: Apply cleaning decision
    if clean_decision.get("action") == "advanced_clean":
        context["data"] = advanced_clean(copy.deepcopy(context["data"]))
        log_step("After Advanced Clean", context["data"])

    # Step 5: Apply transformation decision
    if transform_decision.get("action") == "advanced":
        context["data"] = transform_advanced(copy.deepcopy(context["data"]))
    else:
        context["data"] = transform_basic(copy.deepcopy(context["data"]))

    log_step("After Transformation", context["data"])

    # Step 6: Generate report
    report = generate_report(
        context["data"],
        style=report_decision.get("action", "summary")
    )
    log_step("Final Report", report)

    final_output = {
        "data": context["data"],
        "report": report,
        "history": context["history"]
    }

    # Step 7: Save output automatically
    if save_output:
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        filename = output_dir / f"pipeline_output_{int(time.time())}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Output saved to {filename}")

    return final_output

# Synchronous wrapper for compatibility
def run_pipeline(save_output=True):
    return asyncio.run(run_pipeline_async(save_output=save_output))