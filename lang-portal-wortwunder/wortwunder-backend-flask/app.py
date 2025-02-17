from flask import Flask, jsonify, request
from flask_cors import CORS
from lib.db import get_vocabulary

app = Flask(__name__)

# Update CORS to allow port 8080
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:8080",
                "http://127.0.0.1:8080",
                "http://192.168.178.39:8080",  # Also allow your network IP
            ],
            "methods": ["GET", "POST", "OPTIONS", "HEAD"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "expose_headers": ["Content-Type", "X-Debug"],
        }
    },
)


@app.route("/api/vocabulary")
def vocabulary():
    try:
        theme = request.args.get("theme")
        search = request.args.get("search")

        query = "SELECT * FROM vocabulary"
        params = []
        where_conditions = []

        if theme:
            where_conditions.append("theme = ?")
            params.append(theme)

        if search:
            where_conditions.append("german_word LIKE ?")
            params.append(f"%{search}%")

        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)

        vocab_items = get_vocabulary(query, params)
        print(f"Retrieved {len(vocab_items)} vocabulary items")

        response = jsonify(vocab_items)
        response.headers["X-Debug"] = "Flask-Backend"
        print(f"Sending response with headers: {dict(response.headers)}")
        return response
    except Exception as e:
        print(f"Error in vocabulary endpoint: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server on http://127.0.0.1:5001")
    app.run(debug=True, host="127.0.0.1", port=5001)
