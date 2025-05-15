import swisseph as swe
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pytz

class AstrologyCalculator:
    def __init__(self):
        # Initialize Swiss Ephemeris
        swe.set_ephe_path()
        
    def get_coordinates(self, location):
        """Get latitude and longitude from location string."""
        try:
            geolocator = Nominatim(user_agent="astrella")
            location_data = geolocator.geocode(location)
            if location_data:
                return location_data.latitude, location_data.longitude
            return None
        except GeocoderTimedOut:
            return None

    def calculate_chart(self, birth_date, birth_time, location):
        """Calculate astrological chart points."""
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
            
            # Calculate positions
            sun_pos = swe.calc_ut(jd, swe.SUN)[0]
            moon_pos = swe.calc_ut(jd, swe.MOON)[0]
            
            # Calculate Ascendant
            armc = swe.sidtime(jd) * 15 + lon
            if armc < 0:
                armc += 360
            elif armc > 360:
                armc -= 360
                
            ascendant = swe.house_pos(jd, lat, lon, armc)[0]
            
            # Convert positions to zodiac signs (0-11)
            def get_sign(position):
                return int(position / 30)
            
            def get_sign_name(sign_num):
                signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
                return signs[sign_num]
            
            return {
                "sun": get_sign_name(get_sign(sun_pos)),
                "moon": get_sign_name(get_sign(moon_pos)),
                "ascendant": get_sign_name(get_sign(ascendant))
            }
            
        except Exception as e:
            raise ValueError(f"Error calculating chart: {str(e)}")

# Create a singleton instance
calculator = AstrologyCalculator() 