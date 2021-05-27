from kafka import KafkaConsumer

kafka_servers = ['kafka:9092']
topic = 'test'

consumer = KafkaConsumer(
    topic,
    group_id='test-javier',
    bootstrap_servers=kafka_servers
)

for message in consumer:
    content = message.value.decode('utf-8')
    print(content)
