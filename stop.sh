#!/bin/bash

echo "Stopping AVRO producer..."
ps aux | grep ' producer_avro.py'  | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
echo "Stopping Protobuf producer..."
ps aux | grep ' producer_proto.py' | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1

echo "Stopping docker compose..."
docker compose down
echo "Done!"
echo ""
