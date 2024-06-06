from confluent_kafka import Producer
from src.kafka.config import kafka_config


class KafkaProducer:
    def __init__(self):
        self.producer = Producer(kafka_config)

    def produce_message(self, topic, value):
        self.producer.produce(topic, value.encode('utf-8'))
        self.producer.flush()
