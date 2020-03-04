import threading
import time
import random
import serial
import math
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app)

# serial input
ser = serial.Serial('/dev/cu.usbmodem1421', 115200)

# initialising volume
volume=10

sensors = [0]  #put the number of sensors used
print('sensors length is', len(sensors))
buffer = [0]*20
norms = [0]*len(sensors)

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

def moving_weighted_average(data, bufSize):
    norms[int(data[0])] = abs(math.sqrt( int(data[1])**2 + int(data[2])**2 + int(data[3])**2 )-16000)
    avNorm = sum(norms)/len(norms)
    buffer.append(avNorm)
    avBuffer1 = buffer[-bufSize:]
    avBuffer2 = buffer[-2*bufSize:-bufSize]
    movingAv = sum(avBuffer1)*2/bufSize + sum(avBuffer2)*0.5/bufSize
    # print(movingAv, norms)
    return movingAv/14000

def getSerial():
    while True:
        ser.flushInput()
        borked = False
        line = ser.readline().decode("utf-8")
        data = line.split();
        vals = data[1:]
        idNum = data[:1]
        if (vals == ['1', '1', '1']) or (vals == ['0', '0', '0']):
            borked = True
            print(idNum, 'borked')
        if (len(data) == 4):
            if (int(data[0]) in sensors) and not borked:        
                # vol[0] = moving_average(data, 20)
                volume = moving_weighted_average(data, 10)
                print(volume)


if __name__ == '__main__':
    print("opening websocket")
    sock = threading.Thread(target=sock)
    sock.start()

    print("listening for sensors")
    serialIn = threading.Thread(target=getSerial)
    serialIn.start()