import sqlite3

def view_donations():
    conn = sqlite3.connect('donations.db')
    c = conn.cursor()
    c.execute('SELECT * FROM donations')
    donations = c.fetchall()
    conn.close()
    
    for donation in donations:
        print(donation)

view_donations()
