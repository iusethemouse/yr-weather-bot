"""
A test for the Yr weather API using requests and json.

The product from Yr is LocationFOrecast 2.0.

We can receive the forecast for a location by providing the latitude and longitude.
"""
import requests
import json
import pickle

from pprint import pprint

url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=47.682&lon=9.186"
headers = {
    "User-Agent": "Yr Weather Bot for Telegram | @yr_weather_bot | github.com/iusethemouse/yr-weather-bot"
}

if __name__ == "__main__":
    # response = requests.get(url, headers=headers)
    # data = response.json()
    # save the data to a pickle instead of fetching it every time
    # with open("data.pickle", "wb") as f:
    #     pickle.dump(data, f)

    # read the data back in
    with open("data.pickle", "rb") as f:
        data = pickle.load(f)

    poi = data["properties"]["timeseries"][0]
    # properties = data["properties"]
    # meta = properties["meta"]
    # timeseries = properties["timeseries"]
    # poi = timeseries[0]

    # extract the details
    air_temp = poi["data"]["instant"]["details"]["air_temperature"]
    cloud_coverage = poi["data"]["instant"]["details"]["cloud_area_fraction"]
    wind_speed = poi["data"]["instant"]["details"]["wind_speed"]
    precip_amount_1h = poi["data"]["next_1_hours"]["details"]["precipitation_amount"]

    print(
        f"""\
    Air temperature: {air_temp}
    Cloud coverage: {cloud_coverage}
    Wind speed: {wind_speed}
    Precipitation amount: {precip_amount_1h}\
    """
    )
