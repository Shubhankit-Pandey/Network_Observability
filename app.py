from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_restful import Api, Resource
import asyncio
import json
import random
from datetime import datetime
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)  # Removed async_mode parameter
api = Api(app)

NUM_SUBNETWORKS = 3
NODES_PER_SUBNETWORK = 5

subnets = {f"Subnet{i+1}": [] for i in range(NUM_SUBNETWORKS)}
nodes_data = {}

for i in range(NUM_SUBNETWORKS):
    for j in range(NODES_PER_SUBNETWORK):
        node_name = f"Node_{i+1}_{j+1}"
        subnets[f"Subnet{i+1}"].append(node_name)
        nodes_data[node_name] = None

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

async def listener(queue):
    while True:
        node_name, metrics = await queue.get()
        nodes_data[node_name] = metrics
        socketio.emit('update', json.dumps(nodes_data))
        await asyncio.sleep(1)

def start_simulation():
    queue = asyncio.Queue()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    node_tasks = [node(node_name, queue) for node_name in nodes_data.keys()]
    loop.create_task(listener(queue))
    loop.run_until_complete(asyncio.gather(*node_tasks))

class SubnetMetrics(Resource):
    def get(self, node_name):
        for subnet, nodes in subnets.items():
            if node_name in nodes:
                metrics = {n: nodes_data[n] for n in nodes if nodes_data[n] is not None}
                return jsonify(metrics)
        return {"error": "Node not found in any subnet"}, 404

api.add_resource(SubnetMetrics, '/metrics/<string:node_name>')

@app.route('/')
def index():
    return render_template('index.html', subnets=subnets)

@app.route('/node/<string:node_name>')
def node_view(node_name):
    for subnet, nodes in subnets.items():
        if node_name in nodes:
            return render_template('node.html', node_name=node_name, subnet=subnet, nodes=nodes)
    return "Node not found", 404

if __name__ == "__main__":
    Thread(target=start_simulation).start()
    socketio.run(app, debug=True)
