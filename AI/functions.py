import requests
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime
from geopy.geocoders import Nominatim
"""
Assistants funciton Area
"""
def get_gps_coordinates(address):
    geolocator = Nominatim(user_agent="my_location_app") # Replace "my_location_app" with a unique name
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None


"""
Main funciton Area
"""

#weather agent function include 168hour weather prediction and history forecast
def openweather(Location : str):
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    address = Location
    coordinates = get_gps_coordinates(address)
    if not coordinates :
        print("Location not found.")
        return None
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coordinates[0],
        "longitude": coordinates[1],
        "hourly": "temperature_2m",
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
  
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return ("\nHourly data\n", hourly_dataframe)

def current_time():
    now = datetime.now()
    return "Current time:", now.strftime("%Y-%m-%d %H:%M:%S")

"""
Test function Area
"""
#weather
#print(openweather("Hong Kong, Tsing Yi"))
#Time call
#print(current_time())



