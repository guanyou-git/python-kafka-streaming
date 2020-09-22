docker save -o prometheus.tar prom/prometheus:v2.21.0
docker save -o alertmanager.tar prom/alertmanager:v0.21.0
docker save -o nodeexporter.tar prom/node-exporter:v1.0.1
docker save -o cadvisor.tar gcr.io/cadvisor/cadvisor:v0.37.0
docker save -o grafana.tar grafana/grafana:7.1.5
docker save -o pushgateway.tar prom/pushgateway:v1.2.0
docker save -o caddy.tar stefanprodan/caddy
