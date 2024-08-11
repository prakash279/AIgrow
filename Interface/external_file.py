import requests
from PIL import Image
import time
import io

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZGhydXY0MjU1IiwiYSI6ImNsem5uMjB2ZDBrcWwycXFyN2ZlMjYzZXMifQ.OIsAR6jjDzRdtvJdqqTWCg'
OPENWEATHER_API_KEY = '210ac60a5b2ecf53c3e5c596c0d9d9fa'

last_request_time = 0
request_interval = 60

def fetch_mapbox_image(latitude, longitude):
    global last_request_time

    # Implement rate limiting
    current_time = time.time()
    if current_time - last_request_time < request_interval:
        time.sleep(request_interval - (current_time - last_request_time))
    last_request_time = current_time

    tile_size = 256
    zoom = 15  # Adjust zoom level if needed

    # Adjusted URL for static map image
    tile_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/url-https%3A%2F%2Fdocs.mapbox.com%2Fapi%2Fimg%2Fcustom-marker.png({longitude},{latitude})/{longitude},{latitude},{zoom}/400x300?access_token={MAPBOX_ACCESS_TOKEN}"
    try:
        response = requests.get(tile_url, stream=True, timeout=7)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
    except (requests.exceptions.RequestException, OSError) as e:
        print(f"Error fetching image from {tile_url}: {e}")
        return None

    return img

def fetch_openweather_data(latitude, longitude):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    complete_url = f"{base_url}?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def process_weather_data(data):
    forecast_text = ""
    for forecast in data["list"]:
        dt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather = forecast["weather"][0]["description"]
        forecast_text += f"{dt}: Temperature: {temp:.1f}°C, {weather}\n"
    return forecast_text

def fetch_location(latitude, longitude):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return process_reverse_geocoding(data)
    else:
        return None

def process_reverse_geocoding(data):
    location_text = ""
    c=0
    for i in data:
        name = i["name"]
        state= i["state"]
        country= i["country"]
        
        location_text = f"""Current Location: {name} 
        State: {state}
        Country: {country}"""
    return location_text