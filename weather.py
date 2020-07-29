import requests
import keys


def get_weather(city):
    key = keys.weather_key()
    weather_key = key
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params=params)
    print(response.json())


city = str(input("enter city: "))
get_weather(city)
