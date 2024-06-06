from confluent_kafka.admin import AdminClient, NewTopic
from src.kafka.config import kafka_config


class KafkaAdmin:
    def __init__(self):
        self.admin_client = AdminClient(kafka_config)

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        new_topic = [NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        fs = self.admin_client.create_topics(new_topic)

        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created successfully")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
