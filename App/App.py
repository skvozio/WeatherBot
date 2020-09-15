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
    if request.method == 'POST':
        bot = Bot(BOT_TOKEN)
        update = bot.get_update(request.get_json())
        message = bot.create_message(update)
        bot.send_message(message)
        return 'OK'


if __name__ == '__main__':
    app.run()
