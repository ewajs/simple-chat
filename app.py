import datetime

from flask import Flask, request
from flask_socketio import SocketIO
import sqlite3


app = Flask(__name__)
socketio = SocketIO(app)

conn = sqlite3.connect('test.db')


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/post_msg', methods=['POST'])
def post_msg():
    print(request.json)
    #c = conn.cursor()
    # c.execute("INSERT INTO Message (Date, UserID, MessageText) VALUES (?, 0, ?)",
    #         (datetime.datetime.now().isoformat(), ))
    return "Thanks"


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)
    socketio.run(app, host='0.0.0.0', port=80, debug=True)