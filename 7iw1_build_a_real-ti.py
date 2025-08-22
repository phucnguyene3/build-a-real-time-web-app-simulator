import os
import time
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Simulator data storage
simulator_data = {
    'cpu_usage': 0,
    'memory_usage': 0,
    'network_traffic': 0,
    'request_count': 0
}

# Update simulator data every 1 second
def update_simulator_data():
    while True:
        simulator_data['cpu_usage'] = round(os.popen('python -c "import psutil;print(psutil.cpu_percent())"').read(), 2)
        simulator_data['memory_usage'] = round(os.popen('python -c "import psutil;print(psutil.virtual_memory().percent)"').read(), 2)
        simulator_data['network_traffic'] = round(os.popen('python -c "import psutil;print(psutil.net_io_counters().bytes_recv)"').read(), 2)
        time.sleep(1)
        socketio.emit('update_data', simulator_data)

# Background thread for updating simulator data
socketio.start_background_task(target=update_simulator_data)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)