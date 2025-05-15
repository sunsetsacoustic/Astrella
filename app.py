from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from utils.astrology import calculator
from utils.ai import generate_reading

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
    """Return a list of cities matching the query for the Select2 AJAX location search."""
    query = request.args.get('query', '').lower()
    # Example static city list (expand as needed)
    cities = [
        {'id': 'Houston, Texas', 'name': 'Houston, Texas'},
        {'id': 'New York, New York', 'name': 'New York, New York'},
        {'id': 'Los Angeles, California', 'name': 'Los Angeles, California'},
        {'id': 'Chicago, Illinois', 'name': 'Chicago, Illinois'},
        {'id': 'London, UK', 'name': 'London, UK'},
        {'id': 'Paris, France', 'name': 'Paris, France'},
        {'id': 'Tokyo, Japan', 'name': 'Tokyo, Japan'},
        # ... add more as needed ...
    ]
    results = [city for city in cities if query in city['name'].lower()]
    return jsonify(results)

# ----------------------
# MAIN
# ----------------------

if __name__ == '__main__':
    app.run(debug=True) 