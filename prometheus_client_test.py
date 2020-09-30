from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter
from prometheus_client.exposition import basic_auth_handler
import random
import time


def my_auth_handler(url, method, timeout, headers, data):
    username = 'admin'
    password = 'admin'
    return basic_auth_handler(url, method, timeout, headers, data, username, password)
    
registry = CollectorRegistry()
g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
g.set_to_current_time()

c = Counter('test_thispls', 'Just for testing desc', registry=registry)
c.inc(random.random())


# Pushing metrics to pushgateway
push_to_gateway('pushgateway:9091', job='onlyJOB', registry=registry, handler=my_auth_handler)
