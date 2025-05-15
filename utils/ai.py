import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

# Configure the Gemini API
genai.configure(api_key=api_key)

def generate_reading(chart_data):
    """
    Generate a personalized reading using the Gemini API.
    Returns a formatted HTML string for display.
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        # Construct the prompt
        prompt = f"""
        Based on the following astrological chart data, provide a fun, engaging, and easy-to-read "Core Identity" reading.
        Organize the reading into clear sections with headings, short paragraphs, and bullet points. Use HTML tags for formatting (like <h2>, <h3>, <b>, <ul>, <li>, <br>), and include emojis where appropriate. Do NOT wrap your response in code blocks.

        🌞 <b>Sun Sign:</b> {chart_data['sun']}<br>
        🌙 <b>Moon Sign:</b> {chart_data['moon']}<br>
        ⬆️ <b>Ascendant:</b> {chart_data['ascendant']}<br><br>

        Please include these sections:
        <h2>🌟 Your Core Vibe</h2><br>
        A short, friendly summary of their core personality.<br><br>

        <h2>💪 Stellar Strengths</h2><br>
        A bulleted list of their main strengths.<br><br>

        <h2>🌱 Cosmic Challenges</h2><br>
        A bulleted list of their main challenges or growth areas.<br><br>

        <h2>🔮 A Little Word of Wisdom</h2><br>
        A short, encouraging closing message.<br><br>

        Keep the tone light, positive, and a little whimsical, but also insightful and professional.
        """
        # Generate the response
        response = model.generate_content(prompt)
        text = response.text
        # Remove code block markers if present
        text = re.sub(r'^```[a-zA-Z]*\s*', '', text)  # Remove opening ```
        text = re.sub(r'```$', '', text)               # Remove closing ```
        text = text.strip()
        return text
    except Exception as e:
        raise ValueError(f"Error generating reading: {str(e)}") 