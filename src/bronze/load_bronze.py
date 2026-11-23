
import json
import os
import glob
import hashlib
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


"""
This script loads raw JSON files produced during API extraction
into the SQL Server Bronze layer.

It supports:
    - New records: INSERT
    - Changed records: UPDATE
    - Unchanged records: SKIP
"""


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
driver = os.getenv("SQL_DRIVER")


# --------------------------------------------------
# 2. Create SQL Server connection
# --------------------------------------------------

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection_url = (
    f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
)

engine = create_engine(connection_url)


# --------------------------------------------------
# 3. Generate Pipeline Run ID
# --------------------------------------------------

pipeline_run_id = str(uuid.uuid4())


# --------------------------------------------------
# 4. Find extracted JSON files
# --------------------------------------------------

files = sorted(glob.glob("matches_page_*.json"))

print(f"Found {len(files)} JSON files to process.")


# --------------------------------------------------
# 5. SQL Queries
# --------------------------------------------------

check_query = text("""
    SELECT PayloadHash
    FROM Bronze.RawFootballData
    WHERE SourceSystem = :source_system
      AND Endpoint = :endpoint
""")

insert_query = text("""
    INSERT INTO Bronze.RawFootballData
    (
        SourceSystem,
        Endpoint,
        ResponseJSON,
        PayloadHash,
        LastUpdatedAt,
        PipelineRunID
    )
    VALUES
    (
        :source_system,
        :endpoint,
        :response_json,
        :payload_hash,
        SYSUTCDATETIME(),
        :pipeline_run_id
    )
""")

update_query = text("""
    UPDATE Bronze.RawFootballData
    SET
        ResponseJSON = :response_json,
        PayloadHash = :payload_hash,
        ExtractedAt = SYSUTCDATETIME(),
        LastUpdatedAt = SYSUTCDATETIME(),
        PipelineRunID = :pipeline_run_id
    WHERE SourceSystem = :source_system
      AND Endpoint = :endpoint
""")


# --------------------------------------------------
# 6. Initialize counters
# --------------------------------------------------

inserted_count = 0
updated_count = 0
skipped_count = 0


# --------------------------------------------------
# 7. Process JSON files
# --------------------------------------------------

with engine.begin() as connection:

    for filename in files:

        # Read JSON file
        with open(filename, "r", encoding="utf-8") as file:
            response = json.load(file)

        # Convert JSON payload to string
        response_json = json.dumps(response)

        # Generate SHA-256 hash
        payload_hash = hashlib.sha256(
            response_json.encode("utf-8")
        ).hexdigest()

        # Extract page number from filename
        page_number = filename.replace(
            "matches_page_", ""
        ).replace(".json", "")

        # Construct endpoint
        source_system = "Football-Data.io"

        endpoint = (
            f"/api/v1/seasons/189/matches?page={page_number}"
        )

        # Build reusable parameter dictionary
        params = {
            "source_system": source_system,
            "endpoint": endpoint,
            "response_json": response_json,
            "payload_hash": payload_hash,
            "pipeline_run_id": pipeline_run_id
        }

        # Check whether the record already exists
        result = connection.execute(
            check_query,
            params
        )

        existing_record = result.fetchone()

        # ------------------------------------------
        # INSERT: Record does not exist
        # ------------------------------------------

        if existing_record is None:

            connection.execute(
                insert_query,
                params
            )

            inserted_count += 1

            print(f"Inserted new record: {filename}")

        # ------------------------------------------
        # UPDATE: Record exists but has changed
        # ------------------------------------------

        elif existing_record[0] != payload_hash:

            connection.execute(
                update_query,
                params
            )

            updated_count += 1

            print(f"Updated existing record: {filename}")

        # ------------------------------------------
        # SKIP: Record exists and has not changed
        # ------------------------------------------

        else:

            skipped_count += 1

            print(f"Skipped unchanged record: {filename}")


# --------------------------------------------------
# 8. Display execution summary
# --------------------------------------------------

print("\nBronze Load Summary")
print("------------------")
print(f"Pipeline Run ID: {pipeline_run_id}")
print(f"Files processed: {len(files)}")
print(f"Records inserted: {inserted_count}")
print(f"Records updated: {updated_count}")
print(f"Records skipped: {skipped_count}")

print("\nBronze loading completed successfully!")
