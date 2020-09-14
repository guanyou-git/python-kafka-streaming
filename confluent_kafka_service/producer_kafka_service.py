from confluent_kafka import Producer
import sys
import json


if __name__ == '__main__':
    broker = sys.argv[1]
    topic = sys.argv[2]

    producer = Producer(**{'bootstrap.servers': broker})
    delivery_callback = lambda err, msg: print(err or msg)

    for something in range(1000):
        try:
            producer.produce(topic, str(something),
                             callback=delivery_callback)
        except BufferError:
            print("Local producer queue is full, try again")
        # Serve delivery callback queue
        producer.poll(0)
        # Wait until all messages have been delivered
        producer.flush()

