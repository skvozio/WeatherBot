import os, datetime, emoji
import requests

CLIENT_ID = os.environ['API_CLIENT_ID']
CURRENT_WEATHER_URI = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={ID}'
FORECAST_URI = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&appid={ID}'
print(CLIENT_ID)

def emojize_condition(condition):
    if condition.lower() == 'clear':
        condition = emoji.emojize(':sunny:', use_aliases=True)
    return condition

def get_weather(city):
    message = requests.get(CURRENT_WEATHER_URI
                           .format(city=city, ID=CLIENT_ID)).json()
    if 'message' in message.keys():
        return message['message']
    return message['name'] + ' ' + str(int(message['main']['temp']) - 273) + '°C'


def get_forecast(city):
    message = requests.get(FORECAST_URI.format(city=city, ID=CLIENT_ID)).json()

    daily_temps = [(int(day_temp['temp']['max']-273), day_temp['dt'], day_temp['weather'][0]['main'])
                   for day_temp in message['list'][:3]]
    print(daily_temps)
    response = 'Forecast for ' + message['city']['name'] + ':\n'
    for (temperature, date, condition) in daily_temps:
        date = datetime.datetime.fromtimestamp(date).strftime('%d.%m.%Y')
        response += date + ': ' + str(temperature) + '°C '+ emojize_condition(condition) + '\n'

    return response


if __name__ == '__main__':
    print(get_weather('Бишкек'))
    print(get_forecast('Бишкек,кг'))
    print(emoji.demojize('☀️'))
    print()
    # message = requests.get('https://facebook.com/')
    # print(message.headers)
    # print(message.cookies)
    update = {}
    # if not update['message']:
    #   print('ololol')
