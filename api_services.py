import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_nearby_places(location: str, interests: str) -> list:
    """
    Calls Google Places API to find relevant places based on location and interests.
    """
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "your_google_maps_api_key_here":
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={interests}+tourist+destinations+near+{location}&key={GOOGLE_MAPS_API_KEY}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json().get("results", [])
                places = []
                for r in results[:5]:  # Top 5 places
                    places.append({
                        "name": r.get("name"),
                        "rating": r.get("rating", "N/A"),
                        "types": r.get("types", [])
                    })
                return places if places else [{"name": "No places found matching criteria", "rating": 0, "types": []}]
        except Exception as e:
            print(f"Places API error: {e}")
            
    # Fallback to free Nominatim (OpenStreetMap) API if no Google key
    headers = {"User-Agent": "AI_Travel_Planner_MVP/1.0"}
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={interests}+in+{location}&format=json&limit=5"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results = response.json()
            places = []
            for r in results:
                places.append({
                    "name": r.get("display_name", "").split(",")[0],
                    "rating": "N/A",
                    "types": [r.get("type", "attraction")]
                })
            if places:
                return places
    except Exception as e:
        print(f"OSM API error: {e}")

    # If all APIs fail or have no keys, return an empty list. 
    # The LLM will rely entirely on its internal knowledge rather than fake dummy text.
    return []

def get_distance_and_time(origin: str, destination: str) -> dict:
    """
    Calls Google Distance Matrix API.
    """
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "your_google_maps_api_key_here":
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={destination}&origins={origin}&key={GOOGLE_MAPS_API_KEY}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK" and data["rows"][0]["elements"][0]["status"] == "OK":
                    element = data["rows"][0]["elements"][0]
                    return {
                        "distance_km": element["distance"]["value"] / 1000,
                        "duration_text": element["duration"]["text"],
                        "distance_text": element["distance"]["text"]
                    }
        except Exception as e:
            print(f"Distance API error: {e}")

    # Dummy data
    return {
        "distance_km": 150,
        "duration_text": "3 hours",
        "distance_text": "150 km"
    }

def get_weather(location: str) -> dict:
    """
    Calls OpenWeatherMap API if key is available, else returns mock data.
    """
    if OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "your_openweather_api_key_here":
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temp": data["main"]["temp"],
                    "description": data["weather"][0]["description"].capitalize()
                }
        except Exception as e:
            print(f"Weather API error: {e}")
            
    # Mock data fallback
    return {"temp": 22, "description": "Pleasant and clear"}
