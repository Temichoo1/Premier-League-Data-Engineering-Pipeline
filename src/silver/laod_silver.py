import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def get_sql_connection():

    connection_string = os.getenv("SQL_CONNECTION_STRING")

    if not connection_string:
        raise ValueError(
            "SQL_CONNECTION_STRING is missing from .env"
        )

    connection = pyodbc.connect(connection_string)

    return connection

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

    cursor.executemany(
        sql,
        [
            tuple(record[column] for column in columns)
            for record in records
        ]
    )

    print(
        f"{table_name}: {len(records)} records inserted."
    )
    
if __name__ == "__main__":

    connection = None

    try:

        connection = get_sql_connection()

        print("SQL Server connection successful.")

        # Begin transaction
        connection.autocommit = False

        print("Transaction started.")

        # We haven't loaded any data yet
        # This is just testing the transaction

        connection.commit()

        print("Transaction committed successfully.")

    except Exception as e:

        if connection is not None:

            connection.rollback()

            print("Transaction rolled back.")

        print(f"Error: {e}")

    finally:

        if connection is not None:

            connection.close()

            print("SQL Server connection closed.")