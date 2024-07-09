from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import random
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

# Simulated data generation
nodes_data = {
    'subnet1': [
        {'name': 'Device1', 'ip': '192.168.1.1', 'subnetwork': 'subnet1', 'metrics': {'cpu_usage': 0, 'memory_usage': 0}},
        {'name': 'Device2', 'ip': '192.168.1.2', 'subnetwork': 'subnet1', 'metrics': {'cpu_usage': 0, 'memory_usage': 0}}
    ],
    'subnet2': [
        {'name': 'Device3', 'ip': '192.168.2.1', 'subnetwork': 'subnet2', 'metrics': {'cpu_usage': 0, 'memory_usage': 0}},
        {'name': 'Device4', 'ip': '192.168.2.2', 'subnetwork': 'subnet2', 'metrics': {'cpu_usage': 0, 'memory_usage': 0}}
    ]
}

# Function to update metrics periodically
def update_metrics():
    while True:
        for subnet in nodes_data.values():
            for device in subnet:
                device['metrics']['cpu_usage'] = random.randint(0, 100)
                device['metrics']['memory_usage'] = random.randint(0, 100)
        
        # Emit updated data to all clients
        socketio.emit('metrics_update', nodes_data, namespace='/metrics')
        
        time.sleep(5)  # Update interval in seconds

# Start background thread for updating metrics
thread = threading.Thread(target=update_metrics)
thread.daemon = True
thread.start()

# Routes
@app.route('/')
def admin():
    return render_template('index.html')

@app.route('/node/<string:node_name>')
def node(node_name):
    return render_template('node.html', node_name=node_name)

# SocketIO event handlers
@socketio.on('connect', namespace='/metrics')
def connect():
    emit('metrics_update', nodes_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
