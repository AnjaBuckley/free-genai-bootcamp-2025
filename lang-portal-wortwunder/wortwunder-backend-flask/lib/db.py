import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("german_vocab.db")
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
        conn = sqlite3.connect("german_vocab.db")
        cursor = conn.cursor()

        if query is None:
            query = "SELECT * FROM vocabulary"
            params = []

        print(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        vocab_items = cursor.fetchall()

        print(f"Retrieved {len(vocab_items)} items from database")
        conn.close()

        # Match the actual column names from your database
        columns = ["id", "german_word", "english_translation", "theme"]
        result = []
        for item in vocab_items:
            result.append(dict(zip(columns, item)))

        print("Converted to JSON format:", result)
        return result
    except Exception as e:
        print(f"Error in get_vocabulary: {str(e)}")
        raise
