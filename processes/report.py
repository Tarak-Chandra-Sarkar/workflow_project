def generate_report(data, style="summary"):
    if style == "summary":
        return {
            "total_records": len(data),
            "countries": list(set(row["country"] for row in data)),
        }

    elif style == "detailed":
        return data

    elif style == "executive":
        return f"Processed {len(data)} records across multiple regions."

    return data