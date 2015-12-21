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
    print('a')
    if request.method == 'POST':
        updates = request.get_json()
        chat_id = updates['message']['chat']['id']
        try:
            message_text = updates['message']['text']
        except:
            return 'OK'
        reply_to_message_id = updates['message']['message_id']
        url = 'https://api.telegram.org/bot{TOKEN}/sendMessage'.format(TOKEN=BOT_TOKEN)
        splitted_text = message_text.split(', ')
        if len(splitted_text) != 2:
            requests.post(url, json =dict(chat_id=chat_id, text='Важней всего погода в доме, а что прислал ты - хуета!',
                                          reply_to_message_id=reply_to_message_id))
            #TODO: сделать метод для отправки сообщения
            return 'OK'
        city, country = message_text.split(', ')
        text = str(api_handler.get_weather(city, country))
        response = dict(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id)
        requests.post(url, json=response)

    return 'OK'


if __name__ == '__main__':
    app.run()
