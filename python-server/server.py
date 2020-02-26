from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pickle

app = Flask(__name__, template_folder="./templates", static_folder="./static/dist")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    # return "Hello World!"
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('hello', namespace='/test')
def test_message(message):
    print(message)
    emit('my response', {'data': message['data']})

@socketio.on('broadcast', namespace='/test')
def test_message():
    audioPath = 'sound/0.wav'
    emit('stream', broadcast=True)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)