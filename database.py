import sqlite3
from contextlib import contextmanager

# Updated database name to force Render to create a fresh file with the notes column
DATABASE_NAME = "support_crm_v2.db"

@contextmanager
def get_connection():
    """
    Context manager for SQLite connections.
    Ensures the connection is properly closed after use,
    and rows are returned as dictionaries (sqlite3.Row).
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints (good practice even if unused now)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """
    Initializes the database and creates the 'tickets' table
    if it does not already exist.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT NOT NULL UNIQUE,
        customer_name TEXT NOT NULL,
        customer_email TEXT NOT NULL,
        subject TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL DEFAULT 'Open',
        notes TEXT,
        created_at TEXT NOT NULL
    );
    """

    with get_connection() as conn:
        conn.execute(create_table_query)

    print(f"Database initialized successfully at '{DATABASE_NAME}'")


if __name__ == "__main__":
    # Allows running `python database.py` directly to set up the DB
    init_db()
