# kafka-monitoring

### Çalıştırılacak Komutlar

- sudo apt-get update
- sudo apt-get install python3
- sudo apt install python3-pip
- pip3 install kafka-python 
- git clone https://github.com/vakkassahin/kafka-monitoring.git
-cd kafka-monitoring
- docker-compose up -d
- docker ps
- docker exec -it kafka-monitoring-kafka-1 /bin/bash
- kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
- kafka-topics.sh --list --bootstrap-server localhost:9092
- KAFKA_BROKER=localhost:9092 KAFKA_TOPIC=my-topic THRESHOLD=80 python3 app.py
- docker exec -it kafka-monitoring-zookeeper-1 bash 
- ./bin/zkCli.sh
- create /kafka-manager ""
create /kafka-manager/mutex ""
create /kafka-manager/mutex/locks ""
create /kafka-manager/mutex/leases ""
