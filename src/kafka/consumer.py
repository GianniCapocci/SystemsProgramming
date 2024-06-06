from confluent_kafka import Consumer, KafkaError
from src.kafka.config import kafka_config
import threading


class KafkaConsumer:
    def __init__(self, topic):
        self.consumer = Consumer(kafka_config)
        self.consumer.subscribe([topic])
        self.messages = []

    def consume_messages(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            self.messages.append(msg.value().decode('utf-8'))

    def start(self):
        thread = threading.Thread(target=self.consume_messages, daemon=True)
        thread.start()

    def get_messages(self):
        return self.messages

