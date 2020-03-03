from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app)

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
    volume = 10
    emit('stream', {'data': volume}, broadcast=True)

@socket.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socket.run(app)