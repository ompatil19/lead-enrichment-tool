from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
# from firebase_config import verify_token
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app)
service_port=os.getenv('PORT') or 5000

# API configuration
ENRICHMENT_API_URL = 'https://api.coresignal.com/cdapi/v1/professional_network/company/collect/'
API_KEY = os.getenv('API_KEY')

@app.route('/', methods=['GET'])
def get_hello_world():
    return jsonify(message="Hello, World!")

@app.route('/api/enrich', methods=['POST'])
def enrich_company():
    # Handle actual POST request
    data = request.get_json()
    company_name = data.get('company_name')
    website = data.get('website')

    if not company_name or not website:
        return jsonify({'error': 'Both company_name and website are required'}), 400

    # Validate input format
    if not isinstance(company_name, str) or not isinstance(website, str):
        return jsonify({'error': 'Invalid input format'}), 400

    try:
        # Make a call to the enrichment API
        final_url = ENRICHMENT_API_URL + company_name
        response = requests.get(
            final_url,
            headers={'Authorization': f'Bearer {API_KEY}'}
        )
        response.raise_for_status()  # Check for HTTP errors
        enriched_data = response.json()

        # Return the enriched data in JSON format
        return jsonify(enriched_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=service_port)
