#!/bin/bash

# Check if docker is running
if (! docker stats --no-stream > /dev/null 2>&1); then
    echo "ERROR: Docker Desktop not running"
    exit 1
fi

echo "Stopping AVRO producer..."
ps aux | grep ' producer_avro.py'  | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
echo "Stopping Protobuf producer..."
ps aux | grep ' producer_proto.py' | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1

echo "Stopping docker compose..."
docker compose down
echo "Done!"
echo ""
