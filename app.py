import os
import time
import random
import sys
from kafka import KafkaProducer

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
    # Kafka'ya bağlanmak için bir üretici oluştur
    producer = KafkaProducer(bootstrap_servers=broker)

    def send_usage():
        try:
            cpu, memory = generate_usage()
            message = f"CPU: {cpu}%, Memory: {memory}%"
            producer.send(topic, message.encode())
            print(f"Sent: {message}")

            # Yüksek kullanım durumlarını kontrol et ve alarm gönder
            if cpu >= threshold:
                send_alarm(f"High CPU Usage! CPU: {cpu}%")

            if memory >= threshold:
                send_alarm(f"High Memory Usage! Memory: {memory}%")

        except Exception as e:
            print(f"Error: {e}")

    def send_alarm(alarm_message):
        # Kafka'ya alarm mesajını gönder
        producer.send(topic, alarm_message.encode())
        print(f"Sent Alarm: {alarm_message}")

    def generate_usage():
        cpu = random.randint(0, 100)
        memory = random.randint(0, 100)
        return cpu, memory

    if __name__ == "__main__":
        while True:
            send_usage()
            time.sleep(10)  # Her 10 saniyede bir alarm üret
else:
    print("Error: Broker is not defined.")
    sys.exit(1)
