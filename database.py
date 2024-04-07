import sqlite3

conn = None  # Database connection variable

def connect_to_database():
    global conn
    conn = sqlite3.connect('dbClubsync.db')

def close_connection():
    if conn:
        conn.close()

def create_table():
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clubs (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    college TEXT,
                    venue TEXT)''')
    conn.commit()
    close_connection()

def insert_data(name, college, venue):
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO clubs (name, college, venue) VALUES (?, ?, ?)''', (name, college, venue))
    conn.commit()
    close_connection()

def fetch_clubs():
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM clubs''')
    rows = cursor.fetchall()
    close_connection()
    return rows

def update_data(id, name, college, venue):
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''UPDATE clubs SET name=?, college=?, venue=? WHERE id=?''', (name, college, venue, id))
    conn.commit()
    close_connection()

def delete_data(id):
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM clubs WHERE id=?''', (id,))
    conn.commit()
    close_connection()

def delete_table():
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS clubs''')
    conn.commit()
    close_connection()

def fetch_table_names():
    connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    close_connection()
    return tables
