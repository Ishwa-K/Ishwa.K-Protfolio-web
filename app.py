from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import urllib.request
import urllib.error
import json
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
GMAIL_ADDRESS = "ishwa.kkip@gmail.com"


@app.route("/")
def home():
    return "Ishwa's Portfolio Backend is Running!"


@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400

    if not RESEND_API_KEY:
        return jsonify({
            "success": False,
            "message": "Email service is not configured."
        }), 500

    email_data = {
        "from": "Portfolio <onboarding@resend.dev>",
        "to": [GMAIL_ADDRESS],
        "reply_to": email,
        "subject": f"New Portfolio Message from {name}",
        "text": f"""
New message from your portfolio!

Name: {name}
Email: {email}

Message:
{message}
"""
    }

    try:
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps(email_data).encode("utf-8"),
            headers={
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Ishwa-Portfolio/1.0"
},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))

        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        }), 200

    except urllib.error.HTTPError as e:
        print("RESEND ERROR:", e.code, e.read().decode("utf-8"))
        return jsonify({
            "success": False,
            "message": "Unable to send message."
        }), 500

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        return jsonify({
            "success": False,
            "message": "Unable to send message."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)