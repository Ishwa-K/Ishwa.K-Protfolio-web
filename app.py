from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/")
def home():
    return "Ishwa's Portfolio Backend is Running!"


@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Please fill all fields"}), 400

    try:
        supabase.table("contact_messages").insert({
            "name": name,
            "email": email,
            "message": message
        }).execute()

        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        }), 200

    except Exception as e:
        print("SUPABASE ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Something went wrong. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)