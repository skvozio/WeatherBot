from flask import Flask
import os

TOKEN = os.environ['Token']

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

@app.route('/{token}'.format(TOKEN), methods=['POST'])
def webhook():
    print("It's working")
    return 'OK'