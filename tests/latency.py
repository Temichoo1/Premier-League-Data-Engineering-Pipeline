import pandas as pd
"""
teams = {
    'TeamID': [1, 2, 3, 4],
    'TeamName': [
        'Arsenal',
        'Liverpool',
        'Manchester City',
        'Chelsea'
    ],
    'Country': [
        'England',
        'England',
        'England',
        'England'
    ],
    'Stadium': [
        'Emirates Stadium',
        'Anfield',
        'Etihad Stadium',
        'Stamford Bridge'
    ]
}

df = pd.DataFrame(teams)

print(teams)
"""
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

print(type(data['league']))
print(type(data['seasons']))

print(len(data['seasons']))

print(data['seasons'][0].keys())