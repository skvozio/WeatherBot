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
    
    def _post_method(self, method, data):
        response = requests.post(BASE_URL+method, json=data)
        return 'OK'


    def create_message(self, update):
        print ('create message', update)
        if 'text' in update['message'].keys():
            if any(update['message']['text'].lower() in element for element in
                   ['/help', emoji.emojize(':black_question_mark_ornament:help')]):
                text = 'To receive weather please send a message with city name.\nTo get help send me /help command'
            elif update['message']['text'].lower() == 'city':
                text = 'Please specify your city'
            elif update['message']['text'].startswith('/forecast'):
                city = update['message']['text'].split()
                if len(city) > 1:
                    text = get_forecast(city)
                else:
                    text = 'Please specify a city: /forecast city name'
            else:
                text = get_weather(update['message']['text'])
        else:
            text = 'I understand only text messages'
        keyboard = [[emoji.emojize(':question:help', use_aliases=True)], ['city']]
        reply_keyboard_markup = dict(keyboard=keyboard, one_time_keyboard=True)
        force_reply = dict(force_reply=True)
        message = dict(chat_id=update['chat_id'], reply_to_message_id=update['reply_to_message_id'], text=text,
                       reply_markup=reply_keyboard_markup)
        print(message)

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
