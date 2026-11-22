import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

server = 'T***\SQLEXPRESS' #amend this to your sql server name
database = 'PremierLeagueDW'

connection_string = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)

connection_url = quote_plus(connection_string)

engine = create_engine(
    f'mssql+pyodbc:///?odbc_connect={connection_url}'
)

# Sample football data
teams = {
    'TeamID': [1, 2, 3, 4],
    'TeamName': [
        'Arsenal',
        'Liverpool',
        'Manchester City',
        'Chelsea'
    ],
    'Country': [
        'England',
        'England',
        'England',
        'England'
    ],
    'Stadium': [
        'Emirates Stadium',
        'Anfield',
        'Etihad Stadium',
        'Stamford Bridge'
    ]
}

df = pd.DataFrame(teams)

# Load data into SQL Server
df.to_sql(
    name='Teams',
    con=engine,
    schema='Bronze',
    if_exists='append',
    index=False
)

print("Data successfully loaded into SQL Server!")
