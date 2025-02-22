import sqlite3
import os

# Get the directory containing this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "german_vocab.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database and create tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the vocabulary table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vocabulary (
        id INTEGER PRIMARY KEY,
        german_word TEXT NOT NULL UNIQUE,
        english_translation TEXT NOT NULL,
        theme TEXT NOT NULL
    )
    """)

    # Sample data
    data = [
        ("und", "and", "General"),
        ("sein", "to be", "General"),
        ("ich", "I", "General"),
        ("du", "you", "General"),
        ("er", "he", "General"),
        ("sie", "she/they", "General"),
        ("es", "it", "General"),
        ("wir", "we", "General"),
        ("ihr", "you (plural)", "General"),
        ("haben", "to have", "General"),
        # Example thematic words:
        ("Essen", "food", "Food"),
        ("Trinken", "drink", "Food"),
        ("Reise", "journey/trip", "Travel"),
        ("Zahl", "number", "Numbers"),
    ]

    # Use INSERT OR IGNORE to skip duplicates
    cursor.executemany(
        """
    INSERT OR IGNORE INTO vocabulary (german_word, english_translation, theme)
    VALUES (?, ?, ?)
    """,
        data,
    )

    conn.commit()
    conn.close()

def get_vocabulary(query=None, params=None):
    try:
        print("Attempting to connect to database...")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if query is None:
            query = "SELECT * FROM vocabulary"
            params = []
            
        if params is None:
            params = []
            
        print(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert rows to list of dictionaries
        vocabulary = []
        for row in rows:
            vocabulary.append({
                'id': row['id'],
                'german_word': row['german_word'],
                'english_translation': row['english_translation'],
                'theme': row['theme']
            })
            
        print(f"Retrieved {len(vocabulary)} items from database")
        print("Converted to JSON format:", vocabulary)
        return vocabulary
        
    except Exception as e:
        print(f"Database error: {str(e)}")
        raise e
    
    finally:
        if 'conn' in locals():
            conn.close()

# Initialize the database when this module is imported
init_db()
