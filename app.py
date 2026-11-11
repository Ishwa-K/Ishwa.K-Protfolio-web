from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


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
        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400

    try:
        msg = EmailMessage()

        msg["Subject"] = f"New Portfolio Message from {name}"
        msg["From"] = GMAIL_ADDRESS
        msg["To"] = GMAIL_ADDRESS
        msg["Reply-To"] = email

        msg.set_content(
            f"""
You have received a new message from your portfolio!

Name: {name}
Email: {email}

Message:
{message}
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        }), 200

    except Exception as e:
        print("EMAIL ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Unable to send message. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)