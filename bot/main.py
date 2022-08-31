from pyrogram import Client, emoji, filters
from pprint import pprint
from geopy.geocoders import Nominatim

import requests

HEADERS = {
    "User-Agent": "Yr Weather Bot for Telegram | @yr_weather_bot | github.com/iusethemouse/yr-weather-bot"
}
URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}"

app = Client("yr_bot")


def get_location_name(lat, lon):
    geolocator = Nominatim(user_agent="yr_weather_bot")
    location = geolocator.reverse(f"{lat},{lon}")
    possible_places = ["city", "town", "village"]
    for place in possible_places:
        if place in location.raw["address"]:
            return location.raw["address"][place]

    return "Unknown location"


def extract_weather_data(weather_json):
    if weather_json is None:
        return None

    data = weather_json["properties"]["timeseries"][0]

    # extract the details
    air_temp = data["data"]["instant"]["details"]["air_temperature"]
    cloud_coverage = data["data"]["instant"]["details"]["cloud_area_fraction"]
    wind_speed = data["data"]["instant"]["details"]["wind_speed"]
    precip_amount_1h = data["data"]["next_1_hours"]["details"]["precipitation_amount"]

    return {
        "air_temp": air_temp,
        "cloud_coverage": cloud_coverage,
        "wind_speed": wind_speed,
        "precip_amount_1h": precip_amount_1h,
    }


def get_lat_long(message):
    latitude = f"{float(message.location.latitude):.3f}"
    longitude = f"{float(message.location.longitude):.3f}"

    return latitude, longitude


def get_weather_data(lat, lon):
    url = URL.format(lat, lon)
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def generate_reply_string(weather_data, location_name):
    if weather_data is None:
        return "Could not get weather data."

    return f"""\
        Weather for {location_name}:
• Air temperature: {weather_data["air_temp"]}°C
• Cloud coverage: {weather_data["cloud_coverage"]}%
• Wind speed: {weather_data["wind_speed"]}m/s
• Precipitation in the next hour: {weather_data["precip_amount_1h"] }mm
"""


@app.on_message(filters=filters.command("start"))
def start(client, message):
    client.send_message(
        message.chat.id,
        "Hi! I'm the Yr weather bot.\n\nSend me a location and I'll tell you the weather there.",
    )


@app.on_message()
def echo(client, message):
    if message.location is not None:
        latitude, longitude = get_lat_long(message)
        weather_json = get_weather_data(latitude, longitude)
        location_name = get_location_name(latitude, longitude)
        weather_data = extract_weather_data(weather_json)
        msg_string = generate_reply_string(weather_data, location_name)
    else:
        msg_string = "Please send me your location."

    message.reply_text(msg_string)


app.run()
