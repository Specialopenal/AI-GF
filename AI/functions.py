def get_current_weather(location: str, format: str = "celsius") -> str:
   
    api_key = "Y78dd644b49ec4c8b0baf0ca8895eb50c"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    units = "metric" if format == "celsius" else "imperial"

    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        return f"The current weather in {location} is {weather} with a temperature of {temp}°{'C' if format == 'celsius' else 'F'}."
    else:
        return f"Could not retrieve weather for {location}. Please check the city name or try again later."
    
weather_tool = Tool.from_function(
    func=get_current_weather, 
    name="get_current_weather",
    description="Get the current weather for a city."
)