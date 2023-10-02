from flask import Flask, send_from_directory, request, render_template
from flask_socketio import SocketIO
import random
import time
import sys
from threading import Lock

# Need multiple threads to handle the sensor and server at the same time
thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def send_sensor_data():
    while True:
        sensor_data = {
            'item': 'test item',
            'weight': round(random.uniform(10, 20), 2),
            'cost': round(random.uniform(1, 5), 2)
        }
        socketio.emit('sensor_data', sensor_data)
        time.sleep(5)

# connects to frontend
@app.route('/')
def index():
    return send_from_directory('frontend/public', 'index.html')

# handle connection
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(send_sensor_data)

# handle disconnect
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)