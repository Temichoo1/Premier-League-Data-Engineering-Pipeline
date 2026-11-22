""" Reviewing the data structure and file """

import json
import pandas as pd

# Load raw JSON
with open('matches_raw.json', 'r') as file:
    data = json.load(file)

# Extract matches
matches = data['data']['matches']

# Convert JSON into DataFrame
df = pd.json_normalize(matches)

# 1. Display dimensions
print("DATASET DIMENSIONS")
print(df.shape)

# 2. Display columns
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# 3. Display data types
print("\nDATA TYPES")
print(df.dtypes)

# 4. Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# 5. Check duplicates
print("\nDUPLICATE MATCH IDS")
print(df['match_id'].duplicated().sum())

# 6. Display sample records
print("\nSAMPLE DATA")
print(df.head())

# 7. Check for empty strings
print("\nEMPTY STRING COUNTS")

empty_strings = df.apply(
    lambda column: column.map(
        lambda value: isinstance(value, str) and value.strip() == ''
    ).sum()
)

print(empty_strings[empty_strings > 0])


# 8. Check unique match statuses
print("\nMATCH STATUSES")

print(df['status'].value_counts())


# 9. Check unique seasons
print("\nSEASONS")

print(df['season.year'].unique())


# 10. Check match date range
print("\nMATCH DATE RANGE")

print("Earliest match:", df['match_date'].min())
print("Latest match:", df['match_date'].max())


# 11. Statistical summary of numerical columns
print("\nNUMERICAL DATA SUMMARY")

print(df.describe())


# 12. Check score consistency
print("\nSCORE VALIDATION")

print(
    df[
        df['score.total_goals'] !=
        df['score.home'] + df['score.away']
    ][['match_id', 'score.home', 'score.away', 'score.total_goals']]
)


"""AS THERE IS AN ISSUE WIT THE SCORE VALIDATION WE NEED TO INVESTIGATE"""
#SCORE INVESTIGATION

score_issues = df[
    df['score.total_goals'] !=
    df['score.home'] + df['score.away']
]

print(
    score_issues[
        [
            'match_id',
            'match_date',
            'home_team.team_name',
            'away_team.team_name',
            'score.home',
            'score.away',
            'score.total_goals'
        ]
    ].to_string(index=False)
)

# Find the original JSON record for match 193198 as the total number of goals for this match is incorrect so we need to check why from the original source

for match in matches:

    if match['match_id'] == 193198:

        print("\nORIGINAL JSON RECORD")

        print(
            json.dumps(
                match,
                indent=4
            )
        )

        break

