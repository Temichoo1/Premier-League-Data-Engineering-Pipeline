import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# SQL Server connection details
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
driver = os.getenv("SQL_DRIVER")

# Create connection string
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

# Read original API response
with open("matches_raw.json", "r", encoding="utf-8") as file:
    response = json.load(file) #READS THE FILE AND CONVERTS IT TO A DICTIONARY

# Convert JSON into a string for SQL Server
response_json = json.dumps(response) #This converts the Python dictionary back into a JSON-formatted string, ready to be stored in SQL Server

# Insert into Bronze table
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

with engine.begin() as connection:

    connection.execute(
        insert_query,
        {
            "source_system": "Football-Data.io",
            "endpoint": "/api/v1/seasons/189/matches",
            "response_json": response_json
        }
    )

print("Successfully loaded API response into Bronze!")