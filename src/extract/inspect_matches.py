
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = "https://footballdata.io/api/v1/seasons/189/matches"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

limit = 100
page = 1

while True:

    params = {
        "limit": limit,
        "page": page
    }

    print(f"Extracting page {page}...")

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise Exception(f"API returned an unsuccessful response: {data}")

    matches = data["data"]["matches"]

    print(f"Retrieved {len(matches)} matches.")

    # Save each page separately
    filename = f"matches_page_{page}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Saved {filename}")

    # Stop when fewer than the requested number of records are returned
    if len(matches) < limit:
        print("\nExtraction complete!")
        break

    page += 1
