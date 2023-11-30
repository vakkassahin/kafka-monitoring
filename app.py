
import os
import time
import random
from kafka import KafkaProducer, KafkaConsumer

# Get the environment variables
broker = os.environ.get("KAFKA_BROKER")
topic = os.environ.get("KAFKA_TOPIC")
threshold = int(os.environ.get("THRESHOLD"))

# Create a producer
producer = KafkaProducer(bootstrap_servers=broker)

# Create a consumer
consumer = KafkaConsumer(topic, bootstrap_servers=broker, auto_offset_reset="latest")

# Define a function to generate fake CPU and Memory usage
def generate_usage():
  cpu = random.randint(0, 100)
  memory = random.randint(0, 100)
  return cpu, memory

# Define a function to send the usage data to Kafka
def send_usage():
  cpu, memory = generate_usage()
  message = f"CPU: {cpu}%, Memory: {memory}%"
  producer.send(topic, message.encode())
  print(f"Sent: {message}")

# Define a function to receive the usage data from Kafka and check the threshold
def receive_usage():
  for message in consumer:
    message = message.value.decode()
    print(f"Received: {message}")
    cpu, memory = map(int, message.split(": ")[1].split("%, "))
    if cpu > threshold or memory > threshold:
      print(f"Alarm: High usage detected! {message}")

# Run the producer and consumer in parallel
if _name_ == "_main_":
  while True:
    send_usage()
    receive_usage()
    time.sleep(1)
