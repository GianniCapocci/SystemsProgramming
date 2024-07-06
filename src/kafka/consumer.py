import json
import os
import threading
import time

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError, KafkaException

from src.app import Session
from src.app import app
from src.database import db_util

stop_flag = False


def consume_user_data(consumer, Session):
    global stop_flag
    with app.app_context():
        session = Session()
        try:
            while not stop_flag:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                try:
                    user_data = json.loads(msg.value().decode('utf-8'))
                    db_util.db_register_user(user_data, session)

                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue

        except KeyboardInterrupt:
            print("Shutting down consumer_user")
        finally:
            print("Shutting down consumer_user")
            consumer.close()
            session.close()


def consume_event_data(consumer, Session):
    global stop_flag
    with app.app_context():
        session = Session()
        try:
            while not stop_flag:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())
                try:
                    event_data = json.loads(msg.value().decode('utf-8'))

                    db_util.db_register_event(event_data, session)

                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue

        except KeyboardInterrupt:
            print("Shutting down consumer_event")
        finally:
            print("Shutting down consumer_event")
            consumer.close()
            session.close()


def consume_coupon_data(consumer, Session):
    global stop_flag
    with app.app_context():
        session = Session()
        try:
            while not stop_flag:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                try:
                    coupon_data = json.loads(msg.value().decode('utf-8'))
                    max_retries = 10
                    retry_count = 0

                    while retry_count < max_retries:
                        if db_util.userExists(coupon_data["user_id"], session):
                            all_events_exist = all(
                                db_util.event_exists(selection['event_id'], session) for selection in
                                coupon_data['selections'])
                            if all_events_exist:
                                db_util.db_register_coupon(coupon_data, session)
                                session.commit()
                                break
                            else:
                                retry_count += 1
                                print(f"Retry {retry_count}/{max_retries}: One or more events for the coupon do not exist. Retrying...")
                                time.sleep(2)
                        else:
                            retry_count += 1
                            print(f"Retry {retry_count}/{max_retries}: User does not exist. Retrying...")
                            time.sleep(2)
                    if retry_count == max_retries:
                        print(f"Failed to insert coupon after {max_retries} retries. Events or User may be missing.")
                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue
        except KeyboardInterrupt:
            print("Shutting down consumer_coupon")
        finally:
            print("Shutting down consumer_coupon")
            consumer.close()
            session.close()


def start_consumers(topics):
    global stop_flag
    consumers = []
    for topic, consumer_func in topics.items():
        consumer = KafkaConsumer({
            'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            'group.id': 'my_group',
            'auto.offset.reset': 'earliest'
        })
        consumer.subscribe([topic])
        thread = threading.Thread(target=consumer_func, args=(consumer, Session))
        consumers.append(thread)
        thread.start()

    for consumer in consumers:
        consumer.join()


if __name__ == "__main__":
    try:
        topics = {
            'user_topic': consume_user_data,
            'event_topic': consume_event_data,
            'coupon_topic': consume_coupon_data,
        }
        start_consumers(topics)
    except KeyboardInterrupt:
        print("Received keyboard interrupt. Shutting down all consumers.")
        stop_flag = True
