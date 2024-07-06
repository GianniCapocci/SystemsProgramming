from confluent_kafka.admin import AdminClient, NewTopic


def create_kafka_topics(bootstrap_servers, topics, num_partitions=1, replication_factor=1):
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    existing_topics = admin_client.list_topics(timeout=10).topics

    new_topics = [NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)
                  for topic in topics if topic not in existing_topics]

    if new_topics:
        futures = admin_client.create_topics(new_topics)

        for topic, future in futures.items():
            try:
                future.result()
                print(f"Topic {topic} created")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    else:
        print("No new topics to create")
