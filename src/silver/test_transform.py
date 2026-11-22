import json

from extract_bronze import extract_bronze_data
from transform_matches import flatten_match


bronze_data = extract_bronze_data()

flattened_matches = []

for bronze_record in bronze_data:

    matches = bronze_record["ResponseJSON"]["data"]["matches"]

    for match in matches:

        flattened_match = flatten_match(match)

        flattened_matches.append(flattened_match)


print(f"Total flattened matches: {len(flattened_matches)}")

print("\nFirst flattened match:")

print(json.dumps(flattened_matches[0], indent=4))


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