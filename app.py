import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from handler import handle_message
from states import get_state

load_dotenv()
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")
    print(f"Message recu de {sender}: {incoming}")
    response = MessagingResponse()
    reply = handle_message(sender, incoming)
    response.message(reply)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
