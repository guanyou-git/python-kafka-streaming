from confluent_kafka import Producer
import sys
import os
import json
from time import sleep

from generate_transactions import create_random_transaction

KAFKA_BROKERS = os.environ.get('KAFKA_BROKERS')
KAFKA_TOPIC_RAW = os.environ.get('KAFKA_TOPIC_RAW')
KAFKA_TOPIC_NORULE = os.environ.get('KAFKA_TOPIC_NORULE')
KAFKA_TOPIC_PENDINGVALIDATION = os.environ.get('KAFKA_TOPIC_PENDINGVALIDATION')
KAFKA_TOPIC_TRUE = os.environ.get('KAFKA_TOPIC_TRUE')
KAFKA_TOPIC_FALSE = os.environ.get('KAFKA_TOPIC_FALSE')

KAFKA_CONSUMER_GROUP_ID = os.environ.get('KAFKA_CONSUMER_GROUP_ID')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
TRANSACTION_TIMER = float(os.environ.get('TRANSACTION_TIMER'))

SLEEP_TIME = TRANSACTION_TIMER / TRANSACTIONS_PER_SECOND


if __name__ == '__main__':
    broker = KAFKA_BROKERS
    topic = KAFKA_TOPIC_RAW
    
    producer = Producer(**{'bootstrap.servers': broker})
    delivery_callback = lambda err, msg: print(err or msg)

    while True:
        transaction: dict = create_random_transaction()
        message: str = json.dumps(transaction)
        try:
            producer.produce(topic, message.encode(), callback=delivery_callback)
        except BufferError:
            print("Local producer queue is full, try again")
        producer.poll(0)
        producer.flush()
        sleep(SLEEP_TIME)


