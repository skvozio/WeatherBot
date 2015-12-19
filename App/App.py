from flask import Flask, request
from WeatherAPI import api_handler
import os, requests

BOT_TOKEN = os.environ['TOKEN']

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/{token}'.format(token=BOT_TOKEN), methods=['POST'])
def webhook():
    if request.method == 'POST':
        updates = request.get_json()
        chat_id = updates['message']['chat']['id']
        message_text = updates['message']['text']
        print(message_text)
        city, country = message_text.split(', ')
        print(city, country)
        current_temp = str(api_handler(city, country))
        print(current_temp)
        response = dict(chat_id=chat_id, text=current_temp)
        url = 'https://api.telegram.org/bot{TOKEN}/sendMessage'.format(TOKEN=BOT_TOKEN)
        requests.post(url, json=response)
    #print (updates)

    return 'OK'


if __name__ == '__main__':
    app.run()
