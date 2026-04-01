def transform_basic(data):
    result = []

    for row in data:
        new_row = row.copy()
        new_row["age_group"] = "adult" if new_row["age"] >= 18 else "minor"
        result.append(new_row)

    return result


def transform_advanced(data):
    result = []

    for row in data:
        new_row = row.copy()

        if new_row["country"] == "US":
            new_row["region"] = "North America"
        elif new_row["country"] == "IN":
            new_row["region"] = "Asia"
        else:
            new_row["region"] = "Unknown"

        result.append(new_row)

    return result