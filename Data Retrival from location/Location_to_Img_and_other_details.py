import telebot
import requests
from PIL import Image
import math
import time

BOT_TOKEN = 'api_token'
MAPBOX_ACCESS_TOKEN = 'api_key_token'
OPENWEATHER_API_KEY = 'api_key_token'
bot = telebot.TeleBot(BOT_TOKEN)

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
    zoom = 5 

    x, y = web_mercator_to_tile(longitude, latitude, zoom)

    # tile_url = f"https://api.mapbox.com/v4/mapbox.satellite/{zoom}/{x}/{y}.png?access_token={MAPBOX_ACCESS_TOKEN}"
    tile_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/url-https%3A%2F%2Fdocs.mapbox.com%2Fapi%2Fimg%2Fcustom-marker.png({x},{y})/{x},{y},15/400x300?access_token={MAPBOX_ACCESS_TOKEN}"
    print(tile_url)
    try:
        response = requests.get(tile_url, stream=True, timeout=7)
        response.raise_for_status() 
        img = Image.open(response.raw)
    except (requests.exceptions.RequestException, OSError) as e:
        print(f"Error fetching image from {tile_url}: {e}")
        return None

    return img

def web_mercator_to_tile(lon, lat, zoom):
    x = lon
    y = lat
    return x, y

def fetch_openweather_data(latitude, longitude):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    complete_url = f"{base_url}?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}&units=metric"
    print(complete_url)
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def process_weather_data(data):
    forecast_text = ""
    for forecast in data["list"]:
        dt = forecast["dt"]
        temp = forecast["main"]["temp"]
        weather = forecast["weather"][0]["description"]
        forecast_text += f"{dt}: Temperature: {temp:.1f}°C, {weather}\n"
    return forecast_text


def send_cropped_image(chat_id, cropped_img):
    cropped_img.save('cropped_image.jpg')
    bot.send_photo(chat_id, open('cropped_image.jpg', 'rb'))

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_location = telebot.types.KeyboardButton(text="Send Location", request_location=True)
    keyboard.add(button_location)
    bot.send_message(message.chat.id, "Please share your location:", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    print(latitude, longitude) # Prints Location

    try:
        img = fetch_mapbox_image(latitude, longitude)
        weather_data = fetch_openweather_data(latitude, longitude)
        if img is not None:
            chat_id = message.chat.id  # Access chat ID
            send_cropped_image(chat_id, img)
            forecast_text = process_weather_data(weather_data)
            bot.send_message(chat_id, forecast_text)
        else:
            bot.send_message(message.chat.id, "Failed to fetch image.")
    except Exception as e:
        print(f"Error processing image: {e}")
        bot.send_message(message.chat.id, "An error occurred while processing your request.")

if __name__ == '__main__':
    bot.infinity_polling()
