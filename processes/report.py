'''
dynamic + manual-ready
'''

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

    else:
        return data


if __name__ == "__main__":
    print("Run via main pipeline")