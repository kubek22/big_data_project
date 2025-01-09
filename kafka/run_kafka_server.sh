#!/bin/bash

KAFKA_HOME="/usr/local/kafka"

$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

