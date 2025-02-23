from flask import Flask, jsonify, request
from flask_cors import CORS
from lib.db import get_vocabulary, get_word_groups, add_vocabulary
import os

app = Flask(__name__)

# Configure CORS with specific allowed origins
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5001",  # Flask development server
                "http://localhost:5173",  # Vite development server
                "http://localhost:8080",  # Vite alternative port
                "http://127.0.0.1:5001",
                "http://127.0.0.1:5173",
                "http://127.0.0.1:8080",
                "https://verdant-liger-86fa01.netlify.app",  # Your Netlify production URL
                "https://mimivader.pythonanywhere.com"       # Your PythonAnywhere URL
            ],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    }
)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Wortwunder API"}), 200

@app.route("/api/word-groups")
def word_groups():
    """Get all word groups"""
    try:
        groups = get_word_groups()
        return jsonify(groups)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/vocabulary", methods=["GET", "POST"])
def vocabulary():
    try:
        if request.method == "POST":
            data = request.json
            success = add_vocabulary(
                data["german_word"],
                data["english_translation"],
                data["theme"],
                data["cefr_level"],
                data.get("word_group_id")
            )
            if success:
                return jsonify({"message": "Vocabulary added successfully"}), 201
            else:
                return jsonify({"error": "Failed to add vocabulary"}), 400
        else:
            # Get level from query parameters
            level = request.args.get('level', 'All Levels')
            word_group_id = request.args.get('word_group_id')
            if word_group_id:
                word_group_id = int(word_group_id)
                
            words = get_vocabulary(level=level, word_group_id=word_group_id)
            return jsonify(words)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5006))  # Changed default port to 5006
    app.run(host="0.0.0.0", port=port)
