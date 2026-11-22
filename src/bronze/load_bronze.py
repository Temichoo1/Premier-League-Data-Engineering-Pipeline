
import json
import os
import glob

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

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

# Find all extracted match files
files = sorted(glob.glob("matches_page_*.json"))

insert_query = text("""
    INSERT INTO Bronze.RawFootballData
    (
        SourceSystem,
        Endpoint,
        ResponseJSON
    )
    VALUES
    (
        :source_system,
        :endpoint,
        :response_json
    )
""")

total_files = 0

with engine.begin() as connection:

    for filename in files:

        with open(filename, "r", encoding="utf-8") as file:
            response = json.load(file)

        response_json = json.dumps(response)

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
