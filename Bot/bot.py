import os
import requests

from  WeatherAPI.api_handler import get_weather


TOKEN = os.environ['TOKEN']
BASE_URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)


class Bot(object):
    def __init__(self, token):
        self.token = token
    
    def _post_method(self, method, data):
        response = requests.post(BASE_URL+method, json=data)
        return 'OK'


    def create_message(self, update):
        if update['message']['text']:
            if update['message']['text'].lower() in '/help':
                text = 'To receive weather please send a message with city name.\nTo get help send me /help command'
            else:
                text = get_weather(update['message']['text'])
        else:
            text = 'I understand only text messages'
        message = dict(chat_id=update['chat_id'], reply_to_message_id=update['reply_to_message_id'], text=text)
        return message
                

    def send_message(self, data):
        response = self._post_method('sendMessage', data)
        return 'OK'

    def get_update(self, user_update):
        update = {}
        update['chat_id'] = user_update['message']['chat']['id']
        update['reply_to_message_id'] = user_update['message']['message_id']
        update['message'] = user_update['message']
        return update