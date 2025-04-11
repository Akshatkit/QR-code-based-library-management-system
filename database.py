import sqlite3
from datetime import datetime, timedelta

def initialize_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publisher TEXT,
        year INTEGER,
        available INTEGER DEFAULT 1,
        due_date TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        books_issued INTEGER DEFAULT 0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        book_id TEXT,
        issue_date TEXT,
        due_date TEXT,
        return_date TEXT,
        status TEXT,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (book_id) REFERENCES books (book_id)
    )
    ''')
    
    conn.commit()
    conn.close()

initialize_database()
