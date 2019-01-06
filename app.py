import datetime
import json
import sqlite3

from flask import (
    Flask, 
    request, 
    g, 
    jsonify
)
from flask_socketio import SocketIO


DATABASE = 'test.db'

app = Flask(__name__)
socketio = SocketIO(app)


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
def hello_world():
    return 'Hello, World!'


@app.route('/post_msg', methods=['POST'])
def post_msg():
    t = (datetime.datetime.utcnow().replace(microsecond=0).isoformat(),
         request.json['text'])  # Temporary tuple for insert
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO Message (Date, UserID, MessageText) VALUES (?, 0, ?)", t)
    conn.commit()
    return "Thanks"


@app.route('/get_history', methods=['GET'])
def get_history():
    c = get_db().cursor()
    c.execute("SELECT * FROM Message")
    data = c.fetchall()
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)
    socketio.run(app, host='0.0.0.0', port=80, debug=True)