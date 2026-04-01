'''
hybrid
'''

def basic_clean(data):
    cleaned = []
    for row in data:
        row["age"] = row["age"] or 0
        row["country"] = row["country"] or "UNKNOWN"
        cleaned.append(row)
    return cleaned


def advanced_clean(data):
    # Example: remove unrealistic ages
    return [row for row in data if 0 <= row["age"] <= 100]


if __name__ == "__main__":
    from fetch import fetch_data
    data = fetch_data()
    print(basic_clean(data))