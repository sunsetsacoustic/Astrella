# Astrella

Astrella is a personalized AI-powered astrological reading application that generates your "Core Identity" based on your birth data.

## Features
- Multi-step, user-friendly form for birth data input
- Accurate astrological calculations (Sun, Moon, Ascendant)
- AI-generated, beautifully formatted readings
- Screenshot and share your results
- Clean, modern interface

## Tech Stack
- Backend: Python/Flask
- Frontend: HTML, CSS, JavaScript
- Astrology Calculations: Swiss Ephemeris (pyswisseph)
- AI: Google Gemini API
- Location Services: Geopy

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd astrella
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and add your Gemini API key:
     ```sh
     cp .env.example .env
     # Then edit .env and add your key
     ```

5. **Run the application:**
   ```sh
   python app.py
   ```
   The application will be available at [http://localhost:5000](http://localhost:5000)

## Project Structure
```
astrella/
├── app.py              # Main Flask application
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── utils/              # Utility functions
│   ├── astrology.py    # Astrological calculations
│   └── ai.py           # Gemini API integration
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # Project documentation
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 