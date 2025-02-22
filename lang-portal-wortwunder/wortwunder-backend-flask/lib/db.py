import sqlite3
import os
from typing import List, Dict, Optional

# Get the directory containing this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "german_vocab.db")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # First, get existing vocabulary if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vocabulary'")
    table_exists = cursor.fetchone() is not None
    
    existing_vocab = []
    if table_exists:
        cursor.execute("SELECT german_word, english_translation, theme FROM vocabulary")
        existing_vocab = cursor.fetchall()
        # Drop the existing table to recreate with new schema
        cursor.execute("DROP TABLE IF EXISTS vocabulary")

    # Create word_groups table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS word_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    """)

    # Create vocabulary table with word_group reference
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        german_word TEXT NOT NULL UNIQUE,
        english_translation TEXT NOT NULL,
        theme TEXT NOT NULL,
        word_group_id INTEGER,
        FOREIGN KEY (word_group_id) REFERENCES word_groups(id)
    )
    """)

    # Insert default word groups
    default_groups = [
        ("A1", "Beginner - Basic everyday expressions and phrases"),
        ("A2", "Elementary - Frequently used expressions and simple communication"),
        ("B1", "Intermediate - Clear language on familiar matters"),
        ("B2", "Upper Intermediate - Complex texts and abstract topics"),
        ("C1", "Advanced - Fluent expression for social and professional purposes"),
        ("C2", "Mastery - Understanding and expressing with precision")
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO word_groups (name, description) VALUES (?, ?)",
        default_groups
    )

    # Restore existing vocabulary with basic word group
    if existing_vocab:
        # Add them all to the A1 group initially
        cursor.execute("SELECT id FROM word_groups WHERE name = 'A1'")
        a1_group_id = cursor.fetchone()['id']
        
        for word in existing_vocab:
            cursor.execute(
                """
                INSERT OR IGNORE INTO vocabulary 
                (german_word, english_translation, theme, word_group_id)
                VALUES (?, ?, ?, ?)
                """,
                (word['german_word'], word['english_translation'], word['theme'], a1_group_id)
            )

    # Add some new sample words if we didn't have existing ones
    if not existing_vocab:
        sample_data = [
            ("und", "and", "General", 1),  # A1
            ("sein", "to be", "General", 1),  # A1
            ("ich", "I", "General", 1),  # A1
            ("du", "you", "General", 1),  # A1
            ("er", "he", "General", 1),  # A1
            ("sie", "she/they", "General", 1),  # A1
            ("es", "it", "General", 1),  # A1
            ("wir", "we", "General", 1),  # A1
            ("ihr", "you (plural)", "General", 2),  # A2
            ("haben", "to have", "General", 2),  # A2
            ("Essen", "food", "Food", 1),  # A1
            ("Trinken", "drink", "Food", 1),  # A1
            ("Reise", "journey/trip", "Travel", 2),  # A2
            ("Zahl", "number", "Numbers", 2),  # A2
        ]

        cursor.executemany(
            """
            INSERT OR IGNORE INTO vocabulary 
            (german_word, english_translation, theme, word_group_id)
            VALUES (?, ?, ?, ?)
            """,
            sample_data
        )

    conn.commit()
    conn.close()

def get_word_groups() -> List[Dict]:
    """Get all word groups"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM word_groups ORDER BY name")
    groups = cursor.fetchall()
    conn.close()
    return groups

def add_vocabulary(german_word: str, english_translation: str, theme: str, word_group_id: Optional[int] = None) -> bool:
    """Add a new vocabulary item"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO vocabulary 
            (german_word, english_translation, theme, word_group_id)
            VALUES (?, ?, ?, ?)
            """,
            (german_word, english_translation, theme, word_group_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding vocabulary: {e}")
        return False

def get_vocabulary(query=None, params=None, word_group_id=None):
    """Get vocabulary items with optional filtering"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if query is None:
            query = """
                SELECT v.*, wg.name as word_group_name 
                FROM vocabulary v 
                LEFT JOIN word_groups wg ON v.word_group_id = wg.id
            """
            params = []

        if word_group_id:
            if ' WHERE ' in query:
                query += " AND word_group_id = ?"
            else:
                query += " WHERE word_group_id = ?"
            params = params + [word_group_id]

        cursor.execute(query, tuple(params) if params else ())
        vocabulary = cursor.fetchall()
        conn.close()
        return vocabulary
        
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise

# Initialize the database when this module is imported
init_db()
