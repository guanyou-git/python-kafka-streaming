from confluent_kafka import Consumer, KafkaException
import sys
import json


if __name__ == '__main__':
    broker, group, topics = sys.argv[1], sys.argv[2], sys.argv[3:]
    conf = {'bootstrap.servers': broker, 'group.id': group,
	    'auto.offset.reset': 'earliest'}
    clb = lambda consumer, p: print('Assigned partition:', p)

    consumer = Consumer(conf)
    consumer.subscribe(topics, on_assign=clb)
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(msg.topic(), msg.partition(), msg.offset(),
                      msg.key(), msg.value())
    finally:
        consumer.close() # ... to commit final offsets

