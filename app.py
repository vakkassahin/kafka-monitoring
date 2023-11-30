import os
import time
import random
from kafka import KafkaProducer, KafkaConsumer

# Kafka broker ve topic adını ortam değişkenlerinden al
broker = os.environ.get("KAFKA_BROKER")
topic = os.environ.get("KAFKA_TOPIC")

# Yüksek kullanım alarmı için bir eşik değeri belirle
threshold = int(os.environ.get("THRESHOLD"))

# Broker değişkeninin None olmadığından emin ol
if broker is not None:
    # Kafka'ya bağlanmak için bir üretici ve bir tüketici oluştur
    producer = KafkaProducer(bootstrap_servers=broker)
    consumer = KafkaConsumer(topic, bootstrap_servers=broker, auto_offset_reset="latest")

    # Sahte CPU ve bellek kullanımı verisi üretmek için bir fonksiyon tanımla
    def generate_usage():
        cpu = random.randint(0, 100)
        memory = random.randint(0, 100)
        return cpu, memory

    # Kullanım verisini Kafka'ya göndermek için bir fonksiyon tanımla
    def send_usage():
        try:
            cpu, memory = generate_usage()
            message = f"CPU: {cpu}%, Memory: {memory}%"
            producer.send(topic, message.encode())
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Error: {e}")

    # Kullanım verisini Kafka'dan almak ve eşik değerini kontrol etmek için bir fonksiyon tanımla
    def receive_usage():
        try:
            for message in consumer:
                message = message.value.decode()
                print(f"Received: {message}")
                cpu, memory = map(int, message.split(": ")[1].split("%, "))
                if cpu > threshold and memory > threshold:
                    print(f"Alarm: High usage detected! {message}")
        except Exception as e:
            print(f"Error: {e}")

    # Üretici ve tüketiciyi paralel olarak çalıştır
    if __name__ == "__main__":
        while True:
            send_usage()
            receive_usage()
            time.sleep(1)
else:
    print("Error: Broker is not defined")
