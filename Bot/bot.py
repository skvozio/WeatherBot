import os
import requests

TOKEN = os.environ['TOKEN']
BASE_URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)


class Bot(object):
    def __init__(self, token):
        self.token = token
    
    def _post_method(self, method, data):
        response = requests.post(BASE_URL+method, json=data)
        return 'OK'


    def send_message(self, data):
        response = self._post_method('sendMessage', data)
        return 'OK'

    def get_update(self, user_update):
        update = {}
        update['chat_id'] = user_update['message']['chat']['id']
        update['reply_to_message_id'] = user_update['message']['message_id']
        update['message'] = user_update['message']
        return update