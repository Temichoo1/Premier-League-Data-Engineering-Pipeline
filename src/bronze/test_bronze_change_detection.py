import os
import hashlib
import uuid
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

"""
1. Clean up any previous test record.
2. Insert the original test record.
3. Retrieve its hash.
4. Detect the change.
5. Update the record.
6. Verify the result.
7. Clean up the test record.
This way, the test can be run repeatedly without polluting our actual Bronze table
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
# 3. Create test data
# --------------------------------------------------

test_endpoint = "/test/bronze/change_detection"

original_payload = {
    "match_id": 999999,
    "home_team": "Test FC",
    "away_team": "Example United",
    "home_goals": 2,
    "away_goals": 1
}

changed_payload = {
    "match_id": 999999,
    "home_team": "Test FC",
    "away_team": "Example United",
    "home_goals": 3,
    "away_goals": 1
}

source_system = "Bronze_Test"
pipeline_run_id = str(uuid.uuid4())

# --------------------------------------------------
# 4. Generate payload hashes
# --------------------------------------------------

original_json = json.dumps(original_payload)
changed_json = json.dumps(changed_payload)

original_hash = hashlib.sha256(
    original_json.encode("utf-8")
).hexdigest()

changed_hash = hashlib.sha256(
    changed_json.encode("utf-8")
).hexdigest()


# --------------------------------------------------
# 5. SQL INSERT statement
# --------------------------------------------------

insert_query = text("""
    INSERT INTO Bronze.RawFootballData (
        SourceSystem,
        Endpoint,
        ResponseJSON,
        PayloadHash,
        LastUpdatedAt,
        PipelineRunID
    )
    VALUES (
        :source_system,
        :endpoint,
        :response_json,
        :payload_hash,
        SYSUTCDATETIME(),
        :pipeline_run_id
    )
""")

# --------------------------------------------------
# 6. Insert original test record
# --------------------------------------------------

with engine.begin() as connection:

    connection.execute(
        insert_query,
        {
            "source_system": source_system,
            "endpoint": test_endpoint,
            "response_json": original_json,
            "payload_hash": original_hash,
            "pipeline_run_id": pipeline_run_id
        }
    )
    
# --------------------------------------------------
# 7. SQL SELECT statement
# --------------------------------------------------

check_query = text("""
    SELECT PayloadHash
    FROM Bronze.RawFootballData
    WHERE SourceSystem = :source_system
      AND Endpoint = :endpoint
""")

# --------------------------------------------------
# 8. Compare existing hash with incoming hash
# --------------------------------------------------

with engine.connect() as connection:

    existing_hash = connection.execute(
        check_query,
        {
            "source_system": source_system,
            "endpoint": test_endpoint
        }
    ).scalar()

if existing_hash is None:
    print("Record does not exist.")
    
elif existing_hash == changed_hash:
    print("Record is unchanged. Skipping update.")

else:
    print("Record has changed. Update required.")
    
# --------------------------------------------------
# 8. SQL UPDATE statement
# --------------------------------------------------

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
# 9. Detect changes and update record
# --------------------------------------------------

with engine.begin() as connection:

    existing_hash = connection.execute(
        check_query,
        {
            "source_system": source_system,
            "endpoint": test_endpoint
        }
    ).scalar()

    if existing_hash is None:
        print("Record does not exist.")

    elif existing_hash == changed_hash:
        print("Record is unchanged. Skipping update.")

    else:
        connection.execute(
            update_query,
            {
                "source_system": source_system,
                "endpoint": test_endpoint,
                "response_json": changed_json,
                "payload_hash": changed_hash,
                "pipeline_run_id": pipeline_run_id
            }
        )

        print("Record has changed. Update completed successfully.")
        
# --------------------------------------------------
# 10. SQL DELETE statement (test cleanup)
# --------------------------------------------------

delete_test_query = text("""
    DELETE FROM Bronze.RawFootballData
    WHERE SourceSystem = :source_system
      AND Endpoint = :endpoint
""")

# --------------------------------------------------
# 11. Reset test environment
# --------------------------------------------------

with engine.begin() as connection:

    connection.execute(
        delete_test_query,
        {
            "source_system": source_system,
            "endpoint": test_endpoint
        }
    )

print("Previous test records cleaned up.")

print("Original test record inserted successfully.")


print("Original Hash:", original_hash)
print("Changed Hash:", changed_hash)

print("\nHashes match:", original_hash == changed_hash)