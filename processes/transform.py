'''
hybrid + dynamic modes
'''

def transform_basic(data):
    for row in data:
        row["age_group"] = "adult" if row["age"] >= 18 else "minor"
    return data


def transform_advanced(data):
    for row in data:
        if row["country"] == "US":
            row["region"] = "North America"
        elif row["country"] == "IN":
            row["region"] = "Asia"
        else:
            row["region"] = "Unknown"
    return data