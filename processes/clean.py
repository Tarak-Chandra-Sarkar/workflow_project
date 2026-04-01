def basic_clean(data):
    cleaned = []

    for row in data:
        new_row = row.copy()
        new_row["age"] = new_row["age"] or 0
        new_row["country"] = new_row["country"] or "UNKNOWN"
        cleaned.append(new_row)

    return cleaned


def advanced_clean(data):
    return [
        row.copy()
        for row in data
        if 0 <= row["age"] <= 100
    ]