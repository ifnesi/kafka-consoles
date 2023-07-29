#!/bin/bash

# Check if docker is running
if (! docker stats --no-stream > /dev/null 2>&1); then
    echo "ERROR: Please start Docker Desktop, then run the './start.sh' script"
    exit 1
fi

echo "Starting up docker compose..."
docker compose up -d

echo ""
echo "Confluent Control Center:"
echo "-> http://localhost:9021"
echo ""
sleep 1

echo "Kafka UI:"
echo "-> http://localhost:8888"
echo ""
sleep 1

echo "Conduktor console:"
echo "-> Go to https://signup.conduktor.io and create an user for you"
echo "-> http://localhost:8080 (set the credentials created on the step above)"
echo ""
sleep 1

echo "Waiting to start AVRO and Protobuf producers..."
sleep 20
python3 producer_avro.py > /dev/null &
echo "Started AVRO producer (topic: demo-avro)"
python3 producer_proto.py > /dev/null &
echo "Started Protobuf producer (topic: demo-protobuf)"
echo ""
