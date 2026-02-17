import datetime
import requests

def register_tools(registry):
    registry.register("get_current_time", get_current_time, "Returns the current date and time.")
    registry.register("get_weather", get_weather, "Gets the current weather for a city. Arguments: city (str).")

def get_current_time():
    """Returns the current date and time in a human-readable format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city):
    """Fetches weather from wttr.in."""
    try:
        # Format 3 is concise: "Sunny +25C"
        response = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Error: Could not fetch weather for {city}. Status code: {response.status_code}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
