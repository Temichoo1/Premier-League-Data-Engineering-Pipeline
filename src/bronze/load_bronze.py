
import json
import os
import glob
import hashlib
import uuid

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


"""This script takes the raw JSON files produced during API extraction and loads them into your SQL Server Bronze table"""

load_dotenv()

server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
driver = os.getenv("SQL_DRIVER")

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

pipeline_run_id = str(uuid.uuid4())  ##tells which execution of the pipeline processed the data.

# Find all extracted match files
files = sorted(glob.glob("matches_page_*.json"))

check_query = text("""
    SELECT PayloadHash
    FROM Bronze.RawFootballData
    WHERE SourceSystem = :source_system
      AND Endpoint = :endpoint
""")

total_files = 0

with engine.begin() as connection:

    for filename in files:

        with open(filename, "r", encoding="utf-8") as file:
            response = json.load(file)

        response_json = json.dumps(response)
        
        payload_hash = hashlib.sha256(    #confirms whether the data has changed
        response_json.encode("utf-8")
        ).hexdigest()

        page_number = filename.replace(
            "matches_page_", ""
        ).replace(".json", "")

        connection.execute(
            insert_query,
            {
                "source_system": "Football-Data.io",
                "endpoint": f"/api/v1/seasons/189/matches?page={page_number}",
                "response_json": response_json
            }
        )

        total_files += 1

        print(f"Loaded {filename}")

print(f"\nSuccessfully loaded {total_files} API responses into Bronze!")
