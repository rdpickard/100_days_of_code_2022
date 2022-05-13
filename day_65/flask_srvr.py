import os


from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def route_index():
    return render_template("index.jinja2")


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received MY EVENT json: ' + str(json))
    socketio.emit('pong', json)


if __name__ == '__main__':
    socketio.run(app)
