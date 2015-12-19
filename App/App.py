from flask import Flask
import os

TOKEN = os.environ['TOKEN']

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/{token}'.format(token=TOKEN), methods=['POST'])
def webhook():
    if request.method == 'POST':
        updates = request.get_json()
    print (updates)
    return 'OK'


if __name__ == '__main__':
    app.run()
