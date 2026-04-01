'''
deterministic
'''

def fetch_data():
    # Replace with real source (API, DB, file, etc.)
    data = [
        {"name": "Alice", "age": 25, "country": "US"},
        {"name": "Bob", "age": None, "country": "IN"},
        {"name": "Charlie", "age": 35, "country": None},
    ]
    return data


if __name__ == "__main__":
    print(fetch_data())