# Astrella

A personalized AI-powered astrological reading application that generates your "Core Identity" based on your birth data.

## Features

- Input birth date, time, and location
- Accurate astrological calculations
- AI-generated personalized readings
- Clean, paper-like interface with minimal color accents

## Tech Stack

- Backend: Python/Flask
- Frontend: HTML, CSS, JavaScript
- Astrology Calculations: Swiss Ephemeris (pyswisseph)
- AI: Google Gemini API
- Location Services: Geopy

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/astrella.git
cd astrella
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
astrella/
├── app.py              # Main Flask application
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
├── utils/            # Utility functions
│   ├── astrology.py  # Astrological calculations
│   └── ai.py        # Gemini API integration
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (not in git)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 