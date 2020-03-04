import threading
import time
import random
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app)

volume=10

@app.route('/')
def index():
    # return "Hello World!"
    return render_template('index.html', async_mode=socket.async_mode)

@socket.on('hello', namespace='/test')
def test_message(message):
    print(message)
    emit('response', {'data': message['data']})

@socket.on('broadcast', namespace='/test')
def test_message():
    emit('stream', {'data': volume}, broadcast=True)

@socket.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socket.on('volRequest', namespace='/test')
def emit_volume():
    emit('vol', {'volume': volume})

def sock():
    socket.run(app, host= '0.0.0.0')

def counter():
    while True:
        global volume
        volume = random.randint(-10, 20)
        time.sleep(1)

if __name__ == '__main__':
    sock = threading.Thread(target=sock)
    sock.start()

    counter = threading.Thread(target=counter)
    counter.start()