import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pytz

class AstrologyCalculator:
    """
    Handles astrological calculations using Swiss Ephemeris and geopy for geocoding.
    """
    def __init__(self):
        # Initialize Swiss Ephemeris
        swe.set_ephe_path()
        
    def get_coordinates(self, location):
        """
        Get latitude and longitude from a location string using geopy.
        Returns (lat, lon) tuple or None if not found.
        """
        try:
            geolocator = Nominatim(user_agent="astrella")
            location_data = geolocator.geocode(location)
            if location_data:
                return location_data.latitude, location_data.longitude
            return None
        except GeocoderTimedOut:
            return None

    def calculate_chart(self, birth_date, birth_time, location):
        """
        Calculate Sun, Moon, and Ascendant signs based on birth data.
        Returns a dict with sign names.
        """
        try:
            # Parse date and time
            date_time = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Get coordinates
            coords = self.get_coordinates(location)
            if not coords:
                raise ValueError("Could not find coordinates for the given location")
            
            lat, lon = coords
            
            # Convert to Julian day
            jd = swe.julday(date_time.year, date_time.month, date_time.day,
                          date_time.hour + date_time.minute/60.0)
            
            # Calculate Sun and Moon positions (longitude)
            sun_result = swe.calc_ut(jd, swe.SUN)
            moon_result = swe.calc_ut(jd, swe.MOON)
            sun_pos = float(sun_result[0][0])  # longitude
            moon_pos = float(moon_result[0][0])
            
            # Calculate Ascendant using houses
            houses_result = swe.houses(jd, float(lat), float(lon))
            house_cusps = houses_result[0]
            ascendant = float(house_cusps[0])
            
            # Helper functions for sign calculation
            def get_sign(position):
                return int(float(position) / 30)
            
            def get_sign_name(sign_num):
                signs = [
                    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
                ]
                return signs[sign_num]
            
            return {
                "sun": get_sign_name(get_sign(sun_pos)),
                "moon": get_sign_name(get_sign(moon_pos)),
                "ascendant": get_sign_name(get_sign(ascendant))
            }
            
        except Exception as e:
            raise ValueError(f"Error calculating chart: {str(e)}")

# Singleton instance for use in app
calculator = AstrologyCalculator() 