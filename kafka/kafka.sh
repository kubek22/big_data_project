#!/bin/bash

KAFKA_HOME="/usr/local/kafka"
BROKER="localhost:9092"
TOPIC="sales"
PARTITIONS=1
REPLICATION_FACTOR=1

echo "Creating Kafka topic '$TOPIC'..."
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --bootstrap-server $BROKER \
  --replication-factor $REPLICATION_FACTOR \
  --partitions $PARTITIONS \
  --topic $TOPIC
