import requests
import keys


def get_weather(city):
    try:
        key = keys.WEATHER_KEY()
        weather_key = key
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=params)
        weather = response.json()
        text = "The weather condition of " + str(weather['name']) + " is as follows " + "the overhead condition is " + \
               str(weather['weather'][0]['description']) + " and the temperature in fahrenheit is " + str(weather['main']['temp'])
        return text
    except:
        return "Oops! Could not find any city by this name"
