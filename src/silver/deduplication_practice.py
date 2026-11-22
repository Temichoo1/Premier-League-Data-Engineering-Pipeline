teams = [
    {"TeamID": 135, "TeamName": "Liverpool"},
    {"TeamID": 132, "TeamName": "AFC Bournemouth"},
    {"TeamID": 135, "TeamName": "Liverpool"},
    {"TeamID": 140, "TeamName": "Arsenal"},
    {"TeamID": 132, "TeamName": "AFC Bournemouth"},
    {"TeamID": 150, "TeamName": "Chelsea"}
]

unique_teams = {}

for team in teams:
    unique_teams[team["TeamID"]] = team

unique_teams = list(unique_teams.values())

print(unique_teams)
print(f"Original team records: {len(teams)}")
print(f"Unique team records: {len(unique_teams)}")
