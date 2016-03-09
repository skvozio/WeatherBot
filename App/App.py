import os
import requests


from flask import Flask, request

from WeatherAPI import api_handler
from Bot.bot import Bot




BOT_TOKEN = os.environ['TOKEN']

app = Flask(__name__)




@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/{token}'.format(token=BOT_TOKEN), methods=['POST'])
def webhook():
    print('a')
    if request.method == 'POST':
        bot = Bot(BOT_TOKEN)
        update = bot.get_update(request.get_json())
        message = bot.create_message(update)
        bot.send_message(message)
        return 'OK'

        # chat_id = updates['message']['chat']['id']
        # try:
        #     city = updates['message']['text']
        #     print(city)
        #     reply_to_message_id = updates['message']['message_id']
        #     text = api_handler.get_weather(city)
        #     response = dict(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id)
        #     bot.send_message(response)
        #     return 'OK'
        # except:
        #     print('Exception caught')
        #     return 'OK'


if __name__ == '__main__':
    app.run()
