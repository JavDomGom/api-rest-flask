# api-rest-flask

API REST Flask

## Producer and consumer using internal client

Inside the Kafka Docker container.

Producer:

```bash
~$ echo "Hello world!" | kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

Consumer:

```bash
~$ kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```
