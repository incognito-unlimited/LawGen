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
    """Handle incoming messages from WhatsApp."""
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
