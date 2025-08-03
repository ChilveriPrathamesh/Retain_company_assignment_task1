import sqlite3
from utils.security import hash_password

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

sample_users = [
    ('John Doe', 'john@example.com', 'password123'),
    ('Jane Smith', 'jane@example.com', 'secret456'),
    ('Bob Johnson', 'bob@example.com', 'qwerty789'),
]

for name, email, pwd in sample_users:
    hashed = hash_password(pwd)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed))

conn.commit()
conn.close()
print("Database initialized with sample users (hashed passwords)")
