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

from message_algorithms import save_msg, get_db

app = Flask(__name__)
socketio = SocketIO(app)

clients = []

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    clients.append(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    clients.remove(request.sid)

def send_message_to_client(client_id, data):
    socketio.emit('outer_space_msg', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post_msg', methods=['POST'])
def post_msg():
    print("Posted message")
    save_msg(request.json['text'])
    if clients:
        for client in clients:
            send_message_to_client(client, request.json['text'])

    return "Message saved. Thanks!"


@app.route('/get_history', methods=['GET'])
def get_history():
    c = get_db().cursor()
    c.execute("SELECT * FROM Message")
    data = c.fetchall()
    return jsonify(data)


@socketio.on('post_message')
def handle_message(message: dict):
    try:
        save_msg(message.get('text'))
        return 0
    except Exception as e:
        return "An unexpected error occurred, ¯\_(ツ)_/¯"


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)
