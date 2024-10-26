# models/ai_model.py

import requests
from config import API_KEY, EXTERNAL_USER_ID
import logging

def create_session():
    url = 'https://api.on-demand.io/chat/v1/sessions'
    headers = {'apikey': API_KEY}
    body = {"pluginIds": [], "externalUserId": EXTERNAL_USER_ID}
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        response_data = response.json()
        session_id = response_data.get('data', {}).get('id')
        return session_id
    except requests.exceptions.RequestException as e:
        logging.error(f"Error creating session: {e}")
        return None

def submit_query(session_id, query):
    if not session_id:
        return "Sorry, I'm unable to process your request at the moment."
    url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    headers = {'apikey': API_KEY}
    body = {
        "endpointId": "predefined-openai-gpt4o",
        "query": query,
        "pluginIds": [
            "plugin-1712327325",
            "plugin-1713962163",
            "plugin-1726226353",
            "plugin-1713965172",
            "plugin-1713924030"
        ],
        "responseMode": "sync"
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        response_data = response.json()
        ai_response = response_data.get('data', {}).get('response')
        return ai_response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error submitting query: {e}")
        return "Sorry, I'm unable to process your request at the moment."

def get_ai_response(user_input):
    """Get a response from the AI model using On-Demand API."""
    session_id = create_session()
    ai_response = submit_query(session_id, user_input)
    return ai_response