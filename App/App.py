from flask import Flask
import os

TOKEN = os.environ['TOKEN']

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/{token}'.format(token=TOKEN), methods=['POST'])
def webhook():
    print("It's working")
    return 'OK'


if __name__ == '__main__':
    app.run()
