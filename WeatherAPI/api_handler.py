import os
import requests

CLIENT_ID = os.environ['API_CLIENT_ID']
print(CLIENT_ID)


def get_weather(city):
    message = requests.get('http://api.openweathermap.org/data/2.5/weather?q={city}\
                           &appid={ID}'
                           .format(city=city, ID=CLIENT_ID)).json()
    if 'message' in message.keys():
        return message['message']
    return message['name'] +' '+ str(int(message['main']['temp'])-273) + '°C'


if __name__ == '__main__':
    print(get_weather('Бишкек,кг'))
    update = {}
    #if not update['message']:
     #   print('ololol')
