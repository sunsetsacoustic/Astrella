import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_reading(chart_data):
    """Generate a personalized reading using the Gemini API."""
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Construct the prompt
        prompt = f"""Based on the following astrological chart data, provide a personalized "Core Identity" reading. 
        Focus on the individual's core personality traits, strengths, and potential challenges based on their:
        
        Sun Sign: {chart_data['sun']}
        Moon Sign: {chart_data['moon']}
        Ascendant: {chart_data['ascendant']}
        
        Please provide a thoughtful, insightful reading that:
        1. Explains how these placements work together to create their unique personality
        2. Highlights their natural strengths and potential challenges
        3. Offers guidance on how they can best express their authentic self
        
        Keep the tone warm, encouraging, and professional. Focus on the positive aspects while acknowledging 
        potential challenges as opportunities for growth."""
        
        # Generate the response
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        raise ValueError(f"Error generating reading: {str(e)}") 