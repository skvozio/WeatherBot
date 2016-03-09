import os
import requests
import emoji
import json
import urllib.parse as urlparse
import psycopg2


from WeatherAPI.api_handler import get_weather, get_forecast


TOKEN = os.environ['TOKEN']
BASE_URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

KEYBOARD_OPTIONS = [[emoji.emojize(':question:help', use_aliases=True)], ['/city'], ['/forecast']]
KEYBOARD = dict(keyboard=KEYBOARD_OPTIONS, one_time_keyboard=True)
FORCED = {'force_reply': True,}


class Bot(object):
    def __init__(self, token):
        self.token = token
        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.conn.cursor()

        self.cursor.close()
        print('cursor closed')
        self.conn.close()
        print('connection closed')
    
    def _post_method(self, method, data):
        response = requests.post(BASE_URL+method, json=data)
        return 'OK'

    def _parse_update(self, update):
        message = update['message']
        if 'text' not in message.keys():
            return 'I understand only text messages', KEYBOARD

        if 'reply_to_message' in message.keys():
            if message['reply_to_message']['text'] == 'Please specify your city':
                return get_weather(message['text']), KEYBOARD
            elif message['reply_to_message']['text'] == 'Please specify a city for forecast:':
                return get_forecast(message['text']), KEYBOARD

        if any(update['message']['text'].lower() in element for element in
                   ['/help', emoji.emojize(':black_question_mark_ornament:help')]):
                return ('To receive weather please send a message with city name.\nTo get help send me /help command',
                        KEYBOARD)
        elif message['text'].lower() == 'city':
            return 'Please specify your city', FORCED
        elif update['message']['text'].startswith('/forecast'):
            city = update['message']['text'].split()
            if len(city) > 1:
                return get_forecast(city), KEYBOARD
            else:
                return 'Please specify a city for forecast:', FORCED
        else:
            return get_weather(update['message']['text']), KEYBOARD

    def create_message(self, update):
        print ('create message', update)
        text, reply_markup = self._parse_update(update)
        message = dict(chat_id=update['chat_id'], text=text,
                       reply_markup=reply_markup)
        print(json.dumps(message))

        return message
                

    def send_message(self, data):
        response = self._post_method('sendMessage', data)
        return 'OK'

    def get_update(self, user_update):
        update = {}
        update['chat_id'] = user_update['message']['chat']['id']
        update['user_id'] = user_update['message']['from']['id']
        update['first_name'] = user_update['message']['from']['first_name']
        update['reply_to_message_id'] = user_update['message']['message_id']
        update['message'] = user_update['message']
        #self.cursor.execute('INSERT INTO users (id, first_name) VALUES (%s, %s)', (update['user_id'], update['first_name']))
        #self.cursor.commit()
        self.cursor.close()
        self.conn.close()
        return update
