import os
from dotenv import load_dotenv

load_dotenv()

# On-Demand API credentials
API_KEY = os.getenv('API_KEY')
EXTERNAL_USER_ID = os.getenv('EXTERNAL_USER_ID')

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Flask secret key
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')