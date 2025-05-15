from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from utils.astrology import calculator
from utils.ai import generate_reading
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ----------------------
# ROUTES
# ----------------------

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/get-reading', methods=['POST'])
def get_reading():
    """Generate an astrological reading based on user input."""
    try:
        data = request.get_json()
        birth_date = data.get('birthDate')
        birth_time = data.get('birthTime')
        birth_location = data.get('birthLocation')

        if not all([birth_date, birth_time, birth_location]):
            return jsonify({"error": "Missing required fields"}), 400

        # Calculate astrological chart
        chart_data = calculator.calculate_chart(birth_date, birth_time, birth_location)
        # Generate AI reading
        reading = generate_reading(chart_data)
        return jsonify({"chart": chart_data, "reading": reading})
    except Exception as e:
        # Log the error for debugging
        print("Error in /get-reading:", str(e))
        return jsonify({"error": str(e)}), 400

@app.route('/api/search-location')
def search_location():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    # Use Geoapify Places API for city autocomplete
    url = "https://api.geoapify.com/v1/geocode/autocomplete"
    params = {
        "text": query,
        "type": "city",
        "limit": 10,
        "apiKey": os.environ.get("GEOAPIFY_API_KEY")
    }
    response = requests.get(url, params=params)
    results = []
    for feature in response.json().get("features", []):
        props = feature["properties"]
        display_name = props.get("formatted") or props.get("city") or props.get("name")
        if display_name:
            results.append({"id": display_name, "name": display_name})
    return jsonify(results)

# ----------------------
# MAIN
# ----------------------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port) 