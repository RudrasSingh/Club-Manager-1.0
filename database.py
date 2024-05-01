import sqlite3
from flask import g

def connect_to_database():
    # Get the database connection from the context-local proxy g
    if 'db' not in g:
        g.db = sqlite3.connect('dbClubsync.db')

def get_database():
    # Get the database connection from the context-local proxy g
    if 'db' not in g:
        connect_to_database()
    return g.db

def close_connection():
    # Close the database connection if it exists in the context-local proxy g
    db = g.pop('db', None)
    if db is not None:
        db.close()


#  table 1: Users


def create_users_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    email TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    active INTEGER NOT NULL,
                    college TEXT NOT NULL,
                    contact NUMERIC NOT NULL,
                    banned TEXT,
                    PRIMARY KEY(email)
                    )''')
    db.commit()

def create_user(email, name, active, college, contact, banned):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Users (email, name, active, college, contact, banned) 
                    VALUES (?, ?, ?, ?, ?, ?)''', (email, name, active, college, contact, banned))
    db.commit()

def fetch_users():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Users''')
    rows = cursor.fetchall()
    return rows

def update_user(email, name, active, college, contact, banned):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Users SET name=?, active=?, college=?, contact=?, banned=? WHERE email=?''', 
                   (name, active, college, contact, banned, email))
    db.commit()

def delete_user(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Users WHERE email=?''', (email,))
    db.commit()

def delete_users_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS Users''')
    db.commit()


#  table 2: Clubs


def create_clubs_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Clubs (
                    email TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    college TEXT NOT NULL,
                    active INTEGER NOT NULL,
                    approval TEXT,
                    contact NUMERIC NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    club_head TEXT NOT NULL,
                    ch_contact NUMERIC NOT NULL,
                    club_url TEXT,
                    PRIMARY KEY(email)
                    )''')
    db.commit()

def create_club(email, name, college, active, approval, contact, city, state, club_head, ch_contact, club_url):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Clubs (email, name, college, active, approval, contact, city, state, club_head, ch_contact, club_url) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (email, name, college, active, approval, contact, city, state, club_head, ch_contact, club_url))
    db.commit()

def fetch_clubs():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Clubs''')
    rows = cursor.fetchall()
    return rows

def update_club(email, name, college, active, approval, contact, city, state, club_head, ch_contact, club_url):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Clubs SET name=?, college=?, active=?, approval=?, contact=?, city=?, state=?, club_head=?, ch_contact=?, club_url=? WHERE email=?''', 
                   (name, college, active, approval, contact, city, state, club_head, ch_contact, club_url, email))
    db.commit()

def delete_club(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Clubs WHERE email=?''', (email,))
    db.commit()

def delete_clubs_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS Clubs''')
    db.commit()


#  table 3: Events

def create_events_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Events (
                    club TEXT NOT NULL,
                    fest_name TEXT,
                    event_name TEXT NOT NULL,
                    start_date NUMERIC NOT NULL,
                    end_date NUMERIC,
                    time NUMERIC,
                    details TEXT,
                    event_url TEXT NOT NULL,
                    venue TEXT NOT NULL,
                    fees INTEGER,
                    poster_url TEXT NOT NULL,
                    reg_count NUMERIC NOT NULL,
                    poc TEXT NOT NULL,
                    poc_contact NUMERIC NOT NULL
                    )''')
    db.commit()

def create_event(club, fest_name, event_name, start_date, end_date, time, details, event_url, venue, fees, poster_url, reg_count, poc, poc_contact):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Events (club, fest_name, event_name, start_date, end_date, time, details, event_url, venue, fees, poster_url, reg_count, poc, poc_contact) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (club, fest_name, event_name, start_date, end_date, time, details, event_url, venue, fees, poster_url, reg_count, poc, poc_contact))
    db.commit()

def fetch_events():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Events''')
    rows = cursor.fetchall()
    return rows

def update_event(club, fest_name, event_name, start_date, end_date, time, details, event_url, venue, fees, poster_url, reg_count, poc, poc_contact):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Events SET fest_name=?, event_name=?, start_date=?, end_date=?, time=?, details=?, event_url=?, venue=?, fees=?, poster_url=?, reg_count=?, poc=?, poc_contact=? WHERE club=?''', 
                   (fest_name, event_name, start_date, end_date, time, details, event_url, venue, fees, poster_url, reg_count, poc, poc_contact, club))
    db.commit()

def delete_event(club, event_name):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Events WHERE club=? AND event_name=?''', (club, event_name))
    db.commit()

def delete_events_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS Events''')
    db.commit()

#  table 4: Festival

def create_festival_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Festival (
                    clb_name TEXT NOT NULL,
                    fest_name TEXT,
                    clb_email TEXT NOT NULL,
                    fest_year NUMERIC NOT NULL
                    )''')
    db.commit()

def create_festival(clb_name, fest_name, clb_email, fest_year):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Festival (clb_name, fest_name, clb_email, fest_year) 
                    VALUES (?, ?, ?, ?)''', (clb_name, fest_name, clb_email, fest_year))
    db.commit()

def fetch_festivals():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Festival''')
    rows = cursor.fetchall()
    return rows

def update_festival(clb_name, fest_name, clb_email, fest_year):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Festival SET fest_name=?, clb_email=?, fest_year=? WHERE clb_name=?''', 
                   (fest_name, clb_email, fest_year, clb_name))
    db.commit()

def delete_festival(clb_name):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Festival WHERE clb_name=?''', (clb_name,))
    db.commit()

def delete_festival_table():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DROP TABLE IF EXISTS Festival''')
    db.commit()



# Additional functions:

def fetch_table_names():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return tables


# Main function to create all tables if needed:

def create_all_tables():
    create_users_table()
    create_clubs_table()
    create_events_table()
    create_festival_table()
    
# Main function to delete all tables  if needed:

def delete_all_tables():
    delete_users_table()
    delete_clubs_table()
    delete_events_table()
    delete_festival_table()
    
   
if __name__ == "__main__":
    create_all_tables()    #for creation
   
    # delete_all_tables()    #for deletion
