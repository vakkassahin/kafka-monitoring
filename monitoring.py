import os
import psutil
import time
from kafka import KafkaProducer

kafka_broker = os.environ.get('KAFKA_BROKER', 'localhost:9092')
cpu_threshold = float(os.environ.get('CPU_THRESHOLD', 80))
memory_threshold = float(os.environ.get('MEMORY_THRESHOLD', 80))

producer = KafkaProducer(bootstrap_servers=[kafka_broker])

def monitor():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent

        if cpu_percent > cpu_threshold:
            send_alert(f"High CPU Usage: {cpu_percent}%")

        if memory_percent > memory_threshold:
            send_alert(f"High Memory Usage: {memory_percent}%")

def send_alert(message):
    producer.send('monitoring-alerts', value=message.encode('utf-8'))

if __name__ == "__main__":
    monitor()
