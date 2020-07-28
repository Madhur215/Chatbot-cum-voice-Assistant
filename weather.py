import requests


def get_weather(city):
    weather_key = "Enter your key here"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params=params)
    print(response.json())


city = str(input("enter city: "))
get_weather(city)
