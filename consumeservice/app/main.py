from confluent_kafka import Consumer, KafkaException
import os
import sys
import json

# Use Kafka producer to publish data to Kafka
# Use Kafka consumer to consume data from Kafka

KAFKA_BROKERS = os.environ.get('KAFKA_BROKERS')
KAFKA_TOPIC_RAW = os.environ.get('KAFKA_TOPIC_RAW')
KAFKA_TOPIC_NORULE = os.environ.get('KAFKA_TOPIC_NORULE')
KAFKA_TOPIC_PENDINGVALIDATION = os.environ.get('KAFKA_TOPIC_PENDINGVALIDATION')
KAFKA_TOPIC_TRUE = os.environ.get('KAFKA_TOPIC_TRUE')
KAFKA_TOPIC_FALSE = os.environ.get('KAFKA_TOPIC_FALSE')

KAFKA_CONSUMER_GROUP_ID = os.environ.get('KAFKA_CONSUMER_GROUP_ID')

if __name__ == '__main__':

    topics = [KAFKA_TOPIC_RAW]
    consumer = Consumer({'bootstrap.servers': KAFKA_BROKERS, 'group.id': KAFKA_CONSUMER_GROUP_ID,
			'auto.offset.reset': 'earliest'})
    clb = lambda consumer, p: print('Assigned partition:', p)
    consumer.subscribe(topics, on_assign=clb)

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(msg.topic(), msg.partition(), msg.offset(),
                      msg.key(), msg.value())
    finally:
        consumer.close() # ... to commit final offsets
