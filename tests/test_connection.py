import pyodbc
import pandas as pd
from sqlalchemy import create_engine

server = 'T****\SQLEXPRESS'
database = 'PremierLeagueDW'

connection_string = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
    f'TrustServerCertificate=yes;'
)

try:

    connection = pyodbc.connect(connection_string)

    print("Successfully connected to SQL Server!")

    cursor = connection.cursor()

    cursor.execute("SELECT DB_NAME()")

    result = cursor.fetchone()

    print(f"Connected database: {result[0]}")

    connection.close()

except Exception as e:

    print(f"Connection failed: {e}")
