import os
import requests

CLIENT_ID = os.environ['API_CLIENT_ID']
CLIENT_SECRET = os.environ['API_SECRET']

def get_weather(city, country):
    message = requests.get('http://api.aerisapi.com/observations/{city},{country} \
                           ?client_id=PjkW9QcuMXWbUqH02888X&client_secret=DLDt9gref9bjfkNcV6eDE1YVH6zXjeYRfwULshOw'
                           .format(city=city, country=country)).json()
    print(message['response']['ob']['tempC'])

get_weather('bishkek', 'kg')
