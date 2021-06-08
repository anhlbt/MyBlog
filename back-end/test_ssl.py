from flask import Flask
import ssl
from os.path import dirname, join

root_path = dirname(__file__) 

app = Flask(__name__)


@app.route('/')
def ping():
    return 'pong'


if __name__ == '__main__':
    app.run(ssl_context=('localhost+3.pem', 'localhost+3-key.pem'))
    # app.run(ssl_context='adhoc')