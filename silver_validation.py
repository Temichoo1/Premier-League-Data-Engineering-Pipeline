"""VALIDATING THE SOURCE ATTRIBUTES"""

import json

with open("matches_page_1.json", "r", encoding="utf-8") as file:
    data = json.load(file)

match = data["data"]["matches"][0]

def display_keys(data, prefix=""):
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            display_keys(value, path)
        else:
            print(f"{path}: {value}")

display_keys(match)

