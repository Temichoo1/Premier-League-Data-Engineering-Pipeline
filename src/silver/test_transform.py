import json

from transform_silver import build_silver_datasets
from extract_bronze import extract_bronze_data
from transform_matches import flatten_match


bronze_data = extract_bronze_data()

flattened_matches = []

for bronze_record in bronze_data:

    matches = bronze_record["ResponseJSON"]["data"]["matches"]

    for match in matches:

        flattened_match = flatten_match(match)

        flattened_matches.append(flattened_match)




"""Validate 381 flattened files"""

# Validate flattened data

match_ids = [match["MatchID"] for match in flattened_matches]

print("\n--- Validation Results ---")

print(f"Total matches: {len(flattened_matches)}")

print(f"Unique match IDs: {len(set(match_ids))}")

print(f"Duplicate match IDs: {len(match_ids) - len(set(match_ids))}")

print(f"Missing match IDs: {sum(match['MatchID'] is None for match in flattened_matches)}")

print(f"Missing home team names: {sum(match['HomeTeamName'] is None for match in flattened_matches)}")

print(f"Missing away team names: {sum(match['AwayTeamName'] is None for match in flattened_matches)}")

print(f"Missing match dates: {sum(match['MatchDate'] is None for match in flattened_matches)}")

silver_datasets = build_silver_datasets(flattened_matches)
silver_datasets["Teams"]
silver_datasets["Matches"]
silver_datasets["Leagues"]

print("\n--- Silver Dataset Record Counts ---")

for dataset_name, dataset in silver_datasets.items():
    print(f"{dataset_name}: {len(dataset)} records")

print(f"Total flattened matches: {len(flattened_matches)}")

print("\nFirst flattened match:")

print(json.dumps(flattened_matches[0], indent=4))

print("\n--- Venue Mapping Test ---")

print("\nFirst 5 venues:")

for venue in silver_datasets["Venues"][:20]:
    print(venue)

print("\nFirst 5 matches:")

for match in silver_datasets["Matches"][:20]:
    print({
        "MatchID": match["MatchID"],
        "HomeTeamID": match["HomeTeamID"],
        "AwayTeamID": match["AwayTeamID"],
        "VenueID": match["VenueID"]
    })

missing_venue_ids = sum(
    match["VenueID"] is None
    for match in silver_datasets["Matches"]
)

print(f"\nMatches with missing VenueID: {missing_venue_ids}")

##MISSING DIAGNOSTIC --Matches with missing VenueID: 0
print("\n--- Missing Venue Diagnostic ---")

missing_venue_matches = [
    match
    for match in flattened_matches
    if not match["StadiumName"]
]

print(f"Matches with missing stadium names: {len(missing_venue_matches)}")

print("\nFirst 5 matches with missing stadium names:")

for match in missing_venue_matches[:5]:
    print({
        "MatchID": match["MatchID"],
        "StadiumName": repr(match["StadiumName"]),
        "StadiumLocation": repr(match["StadiumLocation"])
    })