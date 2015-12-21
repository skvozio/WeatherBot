import os
import requests
import emoji

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
        if 'text' in update['message'].keys():
            if any(update['message']['text'].lower() in element.loswer() for element in ['/help', emoji.emojize(':question:help')]):
                text = 'To receive weather please send a message with city name.\nTo get help send me /help command'
            elif update['message']['text'].lower() == 'city':
                text = 'Погода какого города вас интересует'
            else:
                text = get_weather(update['message']['text'])
        else:
            text = 'I understand only text messages'
        keyboard = [[emoji.emojize(':question:help', use_aliases=True)], ['city']]
        reply_keyboard_markup = dict(keyboard=keyboard, one_time_keyboard=True)
        message = dict(chat_id=update['chat_id'], reply_to_message_id=update['reply_to_message_id'], text=text,
                       reply_markup=reply_keyboard_markup)

        return message
                

    def send_message(self, data):
        response = self._post_method('sendMessage', data)
        return 'OK'

    def get_update(self, user_update):
        update = {}
        update['chat_id'] = user_update['message']['chat']['id']
        update['reply_to_message_id'] = user_update['message']['message_id']
        update['message'] = user_update['message']
        print(update)
        return update
