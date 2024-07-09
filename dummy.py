import json
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_device_data(num_devices):
    devices = []
    for i in range(1, num_devices + 1):
        device = {
            "deviceId": str(i),
            "ip": fake.ipv4(),
            "mac": fake.mac_address(),
            "name": f"Device{i}",
            "osVersion": f"OS {random.randint(1, 15)}.{random.randint(1, 10)}",
            "type": random.choice(["Router", "Switch", "Firewall"]),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        }
        devices.append(device)
    return devices

def generate_performance_metrics_data(num_devices):
    performance_metrics = []
    for i in range(1, num_devices + 1):
        metrics = {
            "deviceId": str(i),
            "performanceMetrics": {
                "cpuUsage": f"{random.randint(0, 100)}%",
                "memoryUsage": f"{random.randint(0, 100)}%",
                "bandwidthUtilization": f"{random.randint(0, 100)}%",
                "packetLoss": f"{random.uniform(0, 1):.2%}",
                "latency": f"{random.randint(1, 100)}ms",
                "errorRates": f"{random.uniform(0, 1):.2%}",
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat()
            },
            "networkTrafficMetrics": {
                "trafficVolume": f"{random.randint(100, 1000)}GB",
                "topTalkers": [fake.ipv4() for _ in range(2)],
                "powerStatus": random.choice(["On", "Off"]),
                "uptime": f"{random.randint(1, 365)} days",
                "interfaceStatus": random.choice(["Up", "Down"]),
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat()
            },
            "securityMetrics": {
                "intrusionLogs": [
                    {
                        "log": f"Intrusion detected from IP {fake.ipv4()}",
                        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat()
                    }
                ],
                "authenticationLogs": [
                    {
                        "log": f"Login {'successful' if random.choice([True, False]) else 'failed'} for user {fake.user_name()}",
                        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat()
                    }
                ]
            },
            "eventsAndAlerts": {
                "eventLogs": [fake.sentence() for _ in range(2)],
                "alerts": [fake.sentence() for _ in range(2)],
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat()
            }
        }
        performance_metrics.append(metrics)
    return performance_metrics

def main():
    num_devices = 1000
    devices = generate_device_data(num_devices)
    performance_metrics = generate_performance_metrics_data(num_devices)
    print()
    with open('devices.json', 'w') as f:
        json.dump(devices, f, indent=4)

    with open('performance_metrics.json', 'w') as f:
        json.dump(performance_metrics, f, indent=4)

    print(f"Generated data for {num_devices} devices")

if __name__ == "__main__":
    main()