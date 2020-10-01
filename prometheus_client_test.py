import prometheus_client as prom

req_summary= prom.Summary('namespace_streamingservice1', 'Time spent processing a request')

@req_summary.time()
def process(event, counter1, counter2):
    try:
        time.sleep(random.random())
    except Exception as e:
        print(str(e))
        

if __name__ == '__main__':
    counter1 = prom.Counter('namespace_ingress', 'Counter for ingress')
    counter2 = prom.Counter('namespace_egress', 'Counter for egress')
    prom.start_http_server=(8000)
    while True:
        process(event, counter1, counter2)
        


# from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter
# from prometheus_client.exposition import basic_auth_handler
# import random
# import time


# def my_auth_handler(url, method, timeout, headers, data):
#     username = 'admin'
#     password = 'admin'
#     return basic_auth_handler(url, method, timeout, headers, data, username, password)
    
# registry = CollectorRegistry()
# g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
# g.set_to_current_time()

# c = Counter('test_thispls', 'Just for testing desc', registry=registry)
# c.inc(random.random())


# # Pushing metrics to pushgateway
# push_to_gateway('pushgateway:9091', job='onlyJOB', registry=registry, handler=my_auth_handler)
