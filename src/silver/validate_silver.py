from extract_bronze import extract_bronze_data
from transform_matches import flatten_match
from transform_silver import build_silver_datasets

# Extract Bronze data
bronze_data = extract_bronze_data()

# Flatten the matches
flattened_matches = []

for bronze_record in bronze_data:

    matches = bronze_record["ResponseJSON"]["data"]["matches"]

    for match in matches:
        flattened_match = flatten_match(match)
        flattened_matches.append(flattened_match)

# Build Silver datasets
silver_datasets = build_silver_datasets(flattened_matches)

print("\n========== SILVER DATA QUALITY CHECKS ==========\n")

# Check duplicate primary keys

datasets_to_check = {
    "Leagues": "LeagueID",
    "Seasons": "SeasonID",
    "Teams": "TeamID",
    "Venues": "VenueID",
    "Matches": "MatchID",
    "MatchScores": "MatchID",
    "MatchStatistics": "MatchID"
}

for dataset_name, key_column in datasets_to_check.items():

    records = silver_datasets[dataset_name]

    record_ids = [
        record[key_column]
        for record in records
    ]

    duplicate_count = len(record_ids) - len(set(record_ids))

    print(
        f"{dataset_name}: "
        f"{len(records)} records | "
        f"{duplicate_count} duplicate keys"
    )
    
# Validate team references

team_ids = {
    team["TeamID"]
    for team in silver_datasets["Teams"]
}

invalid_team_references = []

for match in silver_datasets["Matches"]:

    if match["HomeTeamID"] not in team_ids:
        invalid_team_references.append(
            (match["MatchID"], "HomeTeamID")
        )

    if match["AwayTeamID"] not in team_ids:
        invalid_team_references.append(
            (match["MatchID"], "AwayTeamID")
        )

print(
    f"\nInvalid team references: "
    f"{len(invalid_team_references)}"
)
# Validate venue references

venue_ids = {
    venue["VenueID"]
    for venue in silver_datasets["Venues"]
}

invalid_venue_references = []

for match in silver_datasets["Matches"]:

    venue_id = match["VenueID"]

    # Missing venues are permitted
    if venue_id is None:
        continue

    if venue_id not in venue_ids:
        invalid_venue_references.append(
            match["MatchID"]
        )

print(
    f"Invalid venue references: "
    f"{len(invalid_venue_references)}"
)
# Validate MatchScores relationships

match_ids = {
    match["MatchID"]
    for match in silver_datasets["Matches"]
}

score_match_ids = [
    score["MatchID"]
    for score in silver_datasets["MatchScores"]
]

statistics_match_ids = [
    stat["MatchID"]
    for stat in silver_datasets["MatchStatistics"]
]

missing_score_records = match_ids - set(score_match_ids)

missing_statistics_records = match_ids - set(statistics_match_ids)

print(
    f"Matches missing score records: "
    f"{len(missing_score_records)}"
)

print(
    f"Matches missing statistics records: "
    f"{len(missing_statistics_records)}"
)
# Validate score discrepancies

invalid_scores = [
    score
    for score in silver_datasets["MatchScores"]
    if not score["IsScoreValid"]
]

print(
    f"\nMatches with inconsistent source totals: "
    f"{len(invalid_scores)}"
)