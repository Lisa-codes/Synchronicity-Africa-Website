import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('donations.db')
c = conn.cursor()

# Create table for donations
c.execute('''
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_name TEXT,
        phone_number TEXT,
        amount REAL,
        timestamp TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()
