import datetime
import json
import sqlite3

from flask import (
    Flask,
    request,
    g,
    jsonify,
    render_template
)
from flask_socketio import SocketIO

from message_algorithms import save_msg

DATABASE = 'test.db'

app = Flask(__name__)
socketio = SocketIO(app)

# TODO: This module should not know how to connect to a DB


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post_msg', methods=['POST'])
def post_msg():
    save_msg(request.json['text'])
    return "Message saved. Thanks!"


@app.route('/get_history', methods=['GET'])
def get_history():
    c = get_db().cursor()
    c.execute("SELECT * FROM Message")
    data = c.fetchall()
    print(data)
    return jsonify(data)


@socketio.on('post_message')
def handle_message(message: dict):
    save_msg(message.get('text'))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
