import os
import pyodbc
from dotenv import load_dotenv

from extract_bronze import extract_bronze_data
from transform_matches import flatten_match
from transform_silver import build_silver_datasets


                        
SILVER_LOAD_ORDER = [
"Leagues",
"Seasons",
"Teams",
"Venues",
"Matches",
"MatchScores",
"MatchStatistics"
]

SILVER_DELETE_ORDER = [
"MatchStatistics",
"MatchScores",
"Matches",
"Venues",
"Teams",
"Seasons",
"Leagues"
]

load_dotenv()

def get_sql_connection():

    connection_string = os.getenv("SQL_CONNECTION_STRING")

    if not connection_string:
        raise ValueError(
            "SQL_CONNECTION_STRING is missing from .env"
        )

    connection = pyodbc.connect(connection_string)

    return connection


#prepare the Silver datasets
def prepare_silver_datasets():

    print("Extracting Bronze data...")

    bronze_data = extract_bronze_data()

    print("Flattening match data...")

    flattened_matches = []

    for bronze_record in bronze_data:

        matches = bronze_record["ResponseJSON"]["data"]["matches"]

        for match in matches:

            flattened_match = flatten_match(match)

            flattened_matches.append(flattened_match)

    print(
        f"Matches flattened: {len(flattened_matches)}"
    )

    print("Building Silver datasets...")

    silver_datasets = build_silver_datasets(
        flattened_matches
    )

    for dataset_name, records in silver_datasets.items():

        print(
            f"{dataset_name}: {len(records)} records prepared"
        )

    return silver_datasets

##REUSABLE INSERT FUNCTION
def load_dataset(connection, table_name, records):

    if not records:
        print(f"{table_name}: No records to load.")
        return

    columns = list(records[0].keys())

    column_names = ", ".join(columns)

    placeholders = ", ".join(
        ["?"] * len(columns)
    )

    sql = f"""
        INSERT INTO Silver.{table_name}
        ({column_names})
        VALUES ({placeholders});
    """

    cursor = connection.cursor()

    try:

        # Enable IDENTITY_INSERT for Venues
        if table_name == "Venues":

            cursor.execute(
                "SET IDENTITY_INSERT Silver.Venues ON;"
            )

        cursor.executemany(
            sql,
            [
                tuple(record[column] for column in columns)
                for record in records
            ]
        )

        # Disable IDENTITY_INSERT for Venues
        if table_name == "Venues":

            cursor.execute(
                "SET IDENTITY_INSERT Silver.Venues OFF;"
            )

        print(
            f"{table_name}: {len(records)} records inserted."
        )

    except Exception:

        # Ensure IDENTITY_INSERT is disabled if loading fails
        if table_name == "Venues":

            try:

                cursor.execute(
                    "SET IDENTITY_INSERT Silver.Venues OFF;"
                )

            except Exception:
                pass

        raise

#Create load_silver_datasets()
def load_silver_datasets(connection, silver_datasets):

    for table_name in SILVER_LOAD_ORDER:


        records = silver_datasets[table_name]

        print(f"\nLoading Silver.{table_name}...")

        load_dataset(
            connection,
            table_name,
            records
        )

# Clear Silver tables before reloading
def clear_silver_tables(connection):

    cursor = connection.cursor()

    for table_name in SILVER_DELETE_ORDER:

        print(f"Clearing Silver.{table_name}...")

        sql = f"DELETE FROM Silver.{table_name};"

        cursor.execute(sql)

    print("\nAll Silver tables cleared successfully.")

    
if __name__ == "__main__":

    connection = None

    try:

        # Establish SQL Server connection
        connection = get_sql_connection()

        print("SQL Server connection successful.")

        # Disable automatic commits
        connection.autocommit = False

        # Prepare Silver datasets
        silver_datasets = prepare_silver_datasets()

        print("\nStarting Silver refresh...")

        # Clear existing Silver data
        clear_silver_tables(connection)

        # Load all Silver datasets
        load_silver_datasets(
            connection,
            silver_datasets
        )

        # Commit transaction
        connection.commit()

        print("\nSilver refresh committed successfully.")

    except Exception as e:

        if connection is not None:

            connection.rollback()

            print("\nTransaction rolled back.")

        print(f"\nSilver refresh failed: {e}")

    finally:

        if connection is not None:

            connection.close()

            print("SQL Server connection closed.")