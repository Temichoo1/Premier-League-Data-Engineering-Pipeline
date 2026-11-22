import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

url = "https://footballdata.io/api/v1/leagues/15/seasons"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    data = response.json()

    # Save the original API response
    with open("seasons_raw.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Data successfully extracted!")

    # Inspect the JSON structure
    print("\nJSON DATA TYPE:")
    print(type(data))

    print("\nTOP LEVEL KEYS:")
    print(data.keys())

    print("\nSAMPLE JSON RESPONSE:")
    print(json.dumps(data, indent=4)[:3000])
    

else:

    print(f"API Error: {response.status_code}")
    print(response.text)
    
    