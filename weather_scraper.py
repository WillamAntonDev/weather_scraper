import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load the API key from .env
load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")

def get_weather(date, location, fallback_location="Palermo, Italy"):
    if not API_KEY:
        return {"Temp": "N/A", "Wind Speed": "N/A", "Conditions": "API key missing"}

    def fetch(location_query):
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        url = (
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
            f"{location_query}/{formatted_date}?unitGroup=metric&key={API_KEY}&include=days"
      )                   

        response = requests.get(url)
        return response

    # Try original location
    response = fetch(location)
    if response.status_code == 200:
        data = response.json()
        day = data['days'][0]
        return {
            "Location": location,
            "Temp": day.get("temp", "N/A"),
            "Wind Speed": day.get("windspeed", "N/A"),
            "Conditions": day.get("conditions", "N/A")
        }

    # Fallback if original fails
    print(f"⚠️ Failed to get weather for '{location}'. Falling back to '{fallback_location}'...")
    fallback_response = fetch(fallback_location)
    if fallback_response.status_code == 200:
        data = fallback_response.json()
        day = data['days'][0]
        return {
            "Location": fallback_location,
            "Temp": day.get("temp", "N/A"),
            "Wind Speed": day.get("windspeed", "N/A"),
            "Conditions": day.get("conditions", "N/A")
        }

    return {"Location": "Unknown", "Temp": "N/A", "Wind Speed": "N/A", "Conditions": "No data"}

if __name__ == "__main__":
    print("📍 Weather Data Fetcher")
    city = input("Enter city and country (e.g., Florence, Italy): ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
        result = get_weather(date, city)
        print("\n🌦️ Weather Info:")
        for key, value in result.items():
            print(f"{key}: {value}")
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        
def save_to_csv(data, filename="weather_log.csv"):
    df = pd.DataFrame([data])  # Create a single-row DataFrame
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)  # Append without header
    else:
        df.to_csv(filename, index=False)  # First write includes header
    print(f"📂 Saved weather info to '{filename}'")

# 👇 This block must be OUTSIDE of any function
if __name__ == "__main__":
    print("\n📍 Weather Data Fetcher")
    city = input("Enter city and country (e.g., Florence, Italy): ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    weather_data = get_weather(date, city)
    print("\n🌦️ Weather Info:")
    for key, value in weather_data.items():
        print(f"{key}: {value}")

    save_to_csv(weather_data)




