import sqlite3
import pandas as pd

conn = sqlite3.connect('db/database.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS players')
cur.execute('DROP TABLE IF EXISTS players_birthplace')

# Create 'players' table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        birth_date TEXT,
        died_date TEXT,
        debut_year INTEGER,
        still_active BOOLEAN
    )
''')

# Create 'players_birthplace' table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS players_birthplace (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        city TEXT,
        state TEXT,
        birth_date TEXT,
        debut_year INTEGER,
        final_year TEXT
    )
''')

# Load CSV files
players_df = pd.read_csv("csv/players_by_birthyear.csv")
birthplace_df = pd.read_csv("csv/players_by_birthplace.csv")

players_df = players_df.where(pd.notnull(players_df), None)
birthplace_df = birthplace_df.where(pd.notnull(birthplace_df), None)

# Insert into 'players' table
for _, row in players_df.iterrows():
    cur.execute('''
        INSERT INTO players (name, birth_date, died_date, debut_year, still_active)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['name'], row['birth_date'], row['died_date'], row['debut_year'], row['still_active']))

# Insert into 'players_birthplace' table
for _, row in birthplace_df.iterrows():
    cur.execute('''
        INSERT INTO players_birthplace (name, city, state, birth_date, debut_year, final_year)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['name'], row['birth_city'], row['birth_state'], row['birth_date'], row['debut_year'], row['final_year']))

conn.commit()
conn.close()

print("CSV files imported into database.")
