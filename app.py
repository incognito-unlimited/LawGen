'''
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from models.ai_model import get_ai_response
import logging
from config import FLASK_SECRET_KEY
import os

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        response = MessagingResponse()
        msg = response.message()

        logging.info(f"Received message from {from_number}: {incoming_msg}")

        # Get AI response using On-Demand API
        ai_response = get_ai_response(incoming_msg)

        # Send response back to user
        msg.body(ai_response)

        logging.info(f"Sent response to {from_number}: {ai_response}")

        return str(response)
    except Exception as e:
        logging.error(f"Error in webhook: {e}")
        return str(MessagingResponse().message("An error occurred. Please try again later."))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=False, host='0.0.0.0', port=port)
'''
# app.py
from flask import Flask, request
from twilio.rest import Client
import logging
from models.ai_model import get_ai_response
import os

# Twilio setup
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Get incoming message details from Twilio request
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    
    # Fetch AI response
    ai_response = get_ai_response(incoming_msg)
    
    # Send response back to user on WhatsApp
    try:
        message = client.messages.create(
            body=ai_response,
            from_='whatsapp:+14155238886',
            to=sender
        )
        return "Message sent", 200
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return "Error", 500

if __name__ == "__main__":
    app.run(debug=True)
