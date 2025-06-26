# Import the sqlite3 module to interact with SQLite databases
import sqlite3

# Import datetime to work with timestamps
from datetime import datetime

# Define the path to the SQLite database file
DB_PATH = "context.db"

# Initialize the metrics database and create the 'metrics' table if it doesn't exist
def init_metrics_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique ID for each metric entry
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  # Automatically set timestamp
                event_type TEXT NOT NULL,  # Type of event being logged
                value TEXT  # Optional value associated with the event
            );
        ''')

# Log a generic event with an optional value
def log_event(event_type: str, value: str = ""):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO metrics (event_type, value)
            VALUES (?, ?)
        ''', (event_type, value)) 

# Track when a specific tool is used
def track_tool_usage(tool_name: str):
    log_event("Tool used", tool_name)

# Track whether a context lookup was a hit or miss
def track_context_hit(hit: bool):
    log_event("Context HIT" if hit else "Context MISS")

# Track the number of tokens used in a prompt and response
def track_tokens(prompt_tokens: int, response_tokens: int):
    log_event("Tokens - Prompt", str(prompt_tokens))
    log_event("Tokens - Response", str(response_tokens))

# Track the latency of an operation by calculating the time difference
def track_latency(start_time: float):
    latency = round(datetime.now().timestamp() - start_time, 4)
    log_event("Latency", f"{latency}s")

# Track when an error occurs
def track_error():
    log_event("Error occurred")

# Retrieve the most recent metrics from the database, limited by the 'limit' parameter
def get_metrics(limit=100):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT timestamp, event_type, value
            FROM metrics
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()  