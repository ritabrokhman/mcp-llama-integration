# Import the SQLite library for database operations
import sqlite3
# Import datetime for timestamp handling
from datetime import datetime

# Define the path to the SQLite database file
DB_PATH = "context.db"

# Initialize the database and create the context table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique ID for each entry
                tool_name TEXT NOT NULL,               # Name of the tool used
                user_id TEXT,                          # Identifier for the user
                prompt TEXT,                           # The prompt sent to the model
                response TEXT,                         # The model's response
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  # Time of entry
            );
        ''')

# Save a new prompt-response interaction to the database
def save_context(tool_name, user_id, prompt, response):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO context (tool_name, user_id, prompt, response)
            VALUES (?, ?, ?, ?)
        ''', (tool_name, user_id, prompt, response))

# Retrieve the most recent prompt-response pairs for a given user
def get_recent_context(user_id, limit=5):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT prompt, response, timestamp
            FROM context
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        return cursor.fetchall()
