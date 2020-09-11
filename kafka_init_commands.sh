kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 10 --topic test.prototype.event.raw
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 10 --topic test.prototype.event.norule
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 10 --topic test.prototype.event.pendingvalidation
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 10 --topic test.prototype.event.true
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 10 --topic test.prototype.event.false
