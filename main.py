from flask import Flask
from flask import request
from utils import *
from config import credentials
import redis

redis_server = redis.Redis(host=credentials['db']['host'], port=credentials['db']['port'])

app = Flask(__name__)


@app.route('/voucher', methods=['POST'])
def root():
    data = request.get_json()
    return process_request(redis_server, data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
