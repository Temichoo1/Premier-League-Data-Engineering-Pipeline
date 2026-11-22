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

params = {
    "limit": 100,
    "page": 1
}

response = requests.get(
    url,
    headers=headers,
    params=params
)

if response.status_code == 200:

    data = response.json()

    with open("matches_raw.json", "w") as file:

        json.dump(data, file, indent=4)

    print("Extraction successful!")

    print("\nTOP LEVEL KEYS:")
    print(data.keys())

    print("\nDATA STRUCTURE:")
    print(type(data["data"]))

    print("\nSAMPLE RESPONSE:")
    print(json.dumps(data, indent=4)[:5000])

else:

    print("API Error:", response.status_code)
    print(response.text)