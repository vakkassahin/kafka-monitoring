import os
import time
import random
import sys
from kafka import KafkaProducer, KafkaConsumer

# Kafka broker ve topic adını ortam değişkenlerinden al
broker = os.environ.get("KAFKA_BROKER")
topic = os.environ.get("KAFKA_TOPIC")

# Yüksek kullanım alarmı için bir eşik değeri belirle
threshold_str = os.environ.get("THRESHOLD")

# THRESHOLD değeri kontrolü
if threshold_str is not None:
    try:
        threshold = int(threshold_str)
    except ValueError:
        print("Error: THRESHOLD must be a valid integer.")
        sys.exit(1)
else:
    print("Error: THRESHOLD is not defined.")
    sys.exit(1)

# Broker değişkeninin None olmadığından emin ol
if broker is not None:
    # Kafka'ya bağlanmak için bir üretici ve bir tüketici oluştur
    producer = KafkaProducer(bootstrap_servers=broker)

    def send_usage():
        try:
            cpu, memory = generate_usage()
            message = f"CPU: {cpu}%, Memory: {memory}%"
            producer.send(topic, message.encode())
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Error: {e}")

    def generate_usage():
        cpu = random.randint(0, 100)
        memory = random.randint(0, 100)
        return cpu, memory

    # Kafka'ya bağlanmak için bir tüketici oluştur
    consumer = KafkaConsumer(topic, bootstrap_servers=broker, auto_offset_reset="latest")

    def receive_usage():
        try:
            for message in consumer:
                message = message.value.decode()
                print(f"Received: {message}")
                cpu, memory = map(int, message.split(": ")[1].split("%, "))
                if cpu > threshold or memory > threshold:
                    alarm_message = f"Alarm: High usage detected! {message}"
                    print(alarm_message)
                    # Burada alarm durumuyla yapılacak ek işlemleri ekleyebilirsiniz.
        except Exception as e:
            print(f"Error: {e}")

    if __name__ == "__main__":
        while True:
            send_usage()
            receive_usage()
            time.sleep(1)
else:
    print("Error: Broker is not defined.")
    sys.exit(1)
