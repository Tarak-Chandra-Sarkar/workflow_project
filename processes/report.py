# processes/report.py
def generate_report(data, style="summary"):
    if style == "summary":
        return {
            "type": "summary",
            "total_records": len(data),
            "countries": list(set(row["country"] for row in data)),
        }

    elif style == "detailed":
        return {
            "type": "detailed",
            "records": data
        }

    elif style == "executive":
        return {
            "type": "executive",
            "message": f"Processed {len(data)} records across multiple regions."
        }

    else:
        # fallback
        return {
            "type": "custom",
            "data": data
        }