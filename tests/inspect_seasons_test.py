import requests
import pandas as pd
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

    with open("seasons_raw.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Data successfully extracted!")

    print("Top-level keys:")
    print(data.keys())

    print("\nLeague Data Type:")
    print(type(data["league"]))

    print("\nSeasons Data Type:")
    print(type(data["seasons"]))

    print("\nNumber of Seasons:")
    print(len(data["seasons"]))

    print("\nSeason Columns:")
    print(data["seasons"][0].keys())

    seasons_df = pd.DataFrame(data["seasons"])

    print("\nDataFrame Preview:")
    print(seasons_df.head())

else:
    print(f"API Error: {response.status_code}")
    print(response.text)