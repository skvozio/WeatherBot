import os
import requests

CLIENT_ID = os.environ['API_CLIENT_ID']
CLIENT_SECRET = os.environ['API_SECRET']

def get_weather(city, country):
    message = requests.get('http://api.aerisapi.com/observations/{city},{country} \
                           ?client_id={ID}&client_secret={SECRET}'
                           .format(city=city, country=country, ID=CLIENT_ID, SECRET=CLIENT_SECRET)).json()
    return message['response']['ob']['tempC']

get_weather('bishkek', 'kg')
