from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import asyncio
import json
import random
from datetime import datetime
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

fake_metrics = [
    "cpuUsage", "memoryUsage", "bandwidthUtilization", "packetLoss",
    "latency", "errorRates", "trafficVolume", "topTalkers", "powerStatus",
    "uptime", "interfaceStatus"
]

def generate_metrics():
    return {
        "cpuUsage": f"{random.randint(0, 100)}%",
        "memoryUsage": f"{random.randint(0, 100)}%",
        "bandwidthUtilization": f"{random.randint(0, 100)}%",
        "packetLoss": f"{random.uniform(0, 1):.2%}",
        "latency": f"{random.randint(1, 100)}ms",
        "errorRates": f"{random.uniform(0, 1):.2%}",
        "trafficVolume": f"{random.randint(100, 1000)}GB",
        "topTalkers": [f"192.168.1.{random.randint(1, 255)}" for _ in range(2)],
        "powerStatus": random.choice(["On", "Off"]),
        "uptime": f"{random.randint(1, 365)} days",
        "interfaceStatus": random.choice(["Up", "Down"]),
        "timestamp": datetime.now().isoformat()
    }

async def node(name, queue):
    while True:
        metrics = generate_metrics()
        await queue.put((name, metrics))
        await asyncio.sleep(random.uniform(0.5, 2.0))

async def listener(queue, num_nodes):
    nodes_data = {f"Node{i+1}": None for i in range(num_nodes)}
    while True:
        node_name, metrics = await queue.get()
        nodes_data[node_name] = metrics
        socketio.emit('update', json.dumps(nodes_data))
        await asyncio.sleep(1)

def start_simulation():
    num_nodes = 10
    queue = asyncio.Queue()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    node_tasks = [node(f"Node{i+1}", queue) for i in range(num_nodes)]
    loop.create_task(listener(queue, num_nodes))
    loop.run_until_complete(asyncio.gather(*node_tasks))

@app.route('/test')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    Thread(target=start_simulation).start()
    socketio.run(app)
