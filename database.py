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


def create_user(email, name, active, college, contact, profile_pic_url,banned):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Users (email, name, active, college, contact, profile_pic_url, banned) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (email, name, active, college, contact, profile_pic_url, banned))
    db.commit()

def fetch_users():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Users''')
    rows = cursor.fetchall()
    return rows

def update_user(email, name, active, college, contact, profile_pic_url,banned):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Users SET name=?, active=?, college=?, contact=?, profile_pic_url=?, banned=? WHERE email=?''', 
                   (name, active, college, contact, profile_pic_url, banned, email))
    db.commit()

def delete_user(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Users WHERE email=?''', (email,))
    db.commit()


#  table 2: Clubs

def create_club(email, name, college, active, approval, contact, city, state, details, logo_url, club_head, ch_contact, club_url):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Clubs (email, name, college, active, approval, contact, city, state, details, logo_url, club_head, ch_contact, club_url) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (email, name, college, active, approval, contact, city, state, details, logo_url, club_head, ch_contact, club_url))
    db.commit()

def fetch_clubs():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Clubs''')
    rows = cursor.fetchall()
    return rows

def update_club(email, name, college, active, approval, contact, city, state, details, logo_url, club_head, ch_contact, club_url):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Clubs SET name=?, college=?, active=?, approval=?, contact=?, city=?, state=?, details=?, logo_url=?, club_head=?, ch_contact=?, club_url=? WHERE email=?''', 
                   (name, college, active, approval, contact, city, state, details, logo_url, club_head, ch_contact, club_url, email))
    db.commit()

def delete_club(email):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Clubs WHERE email=?''', (email,))
    db.commit()

#  table 3: Events
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

#  table 4: Festival

def create_festival(clb_name, fest_name, clb_email, fest_year, fest_logo_url):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Festival (clb_name, fest_name, clb_email, fest_year, fest_logo_url) 
                    VALUES (?, ?, ?, ?, ?)''', (clb_name, fest_name, clb_email, fest_year, fest_logo_url))
    db.commit()

def fetch_festivals():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Festival''')
    rows = cursor.fetchall()
    return rows

def update_festival(clb_name, fest_name, clb_email, fest_year, fest_logo_url):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Festival SET fest_name=?, clb_email=?, fest_year=?, fest_logo_url=? WHERE clb_name=?''', 
                   (fest_name, clb_email, fest_year, clb_name, fest_logo_url))
    db.commit()

def delete_festival(clb_name):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Festival WHERE clb_name=?''', (clb_name,))
    db.commit()

#  table 5: Reg_details

def create_Reg_details(reg_number, name, email, contact, event_name):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Reg_details (reg_number, name, email, contact, event_name) 
                    VALUES (?, ?, ?, ?, ?)''', (reg_number, name, email, contact, event_name))
    db.commit()

def fetch_Reg_details():
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Reg_details''')
    rows = cursor.fetchall()
    return rows

def update_Reg_details(reg_number, name, email, contact, event_name):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''UPDATE Reg_detailsSET reg_number=?, name=?, email=?, contact=?, event_name=?''', 
                   (reg_number, name, email, contact, event_name))
    db.commit()

def delete_Reg_details(reg_number):
    db = get_database()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Reg_details WHERE clb_name=?''', (reg_number,))
    db.commit()

# Additional functions:

def fetch_table_names():
    db = get_database()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return tables
