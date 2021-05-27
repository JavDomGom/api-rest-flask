from kafka import KafkaProducer

kafka_servers = ['kafka:9092']
topic = 'test'

producer = KafkaProducer(
    bootstrap_servers=kafka_servers
)
producer.send(topic, b'Hello, World!')
producer.send(topic, key=b'message-two', value=b'This is Kafka-Python')
