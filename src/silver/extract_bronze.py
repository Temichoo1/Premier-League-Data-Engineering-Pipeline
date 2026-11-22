import os
import json

import pyodbc
from dotenv import load_dotenv


load_dotenv()


def extract_bronze_data():

    connection_string = os.getenv("SQL_CONNECTION_STRING")

    if not connection_string:
        raise ValueError("SQL_CONNECTION_STRING is missing from .env")

    connection = pyodbc.connect(connection_string)

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                RawDataID,
                Endpoint,
                ResponseJSON,
                ExtractedAt
            FROM Bronze.RawFootballData
            ORDER BY RawDataID;
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        bronze_data = []

        for row in rows:

            bronze_data.append({
                "RawDataID": row.RawDataID,
                "Endpoint": row.Endpoint,
                "ResponseJSON": json.loads(row.ResponseJSON), #converts the text to python objects
                "ExtractedAt": row.ExtractedAt
            })

        return bronze_data

    finally:
        connection.close()


if __name__ == "__main__":

    data = extract_bronze_data()
    print(type(data))
    print(type(data[0]))
    print(type(data[0]["ResponseJSON"]))
    print(type(data[0]["ResponseJSON"]["data"]))
    print(type(data[0]["ResponseJSON"]["data"]["matches"]))
    print(type(data[0]["ResponseJSON"]["data"]["matches"][0]))

    print(f"Records extracted from Bronze: {len(data)}")

    if data:

        first_record = data[0]

        print("\nFirst Bronze record:")
        print(f"RawDataID: {first_record['RawDataID']}")
        print(f"Endpoint: {first_record['Endpoint']}")

        matches = first_record["ResponseJSON"]["data"]["matches"]

        print(f"Matches contained in first record: {len(matches)}")

        print("\nFirst match:")
        print(json.dumps(matches[0], indent=4))