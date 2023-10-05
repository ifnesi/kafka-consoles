#!/bin/bash

# Validate input arguments
by_pass_conduktor=0
if [ $# -gt 0 ]; then
    if [ $1 == '-nc' ]; then
        by_pass_conduktor=1
        echo ""
        echo "By passing Conduktor platform demo"
        echo ""
    elif [ $1 == '-h' ]; then
        echo ""
        echo "Usage:"
        echo "  $0 -nc # Bypass the Conduktor platform demo"
        echo "  $0 -h  # View help"
        echo ""
        exit 1
    else
        echo ""
        echo "ERROR: Invalid argument"
        echo ""
        exit 1
    fi
fi

if [ $by_pass_conduktor -eq 0 ]; then
    echo "Checking for mandatory environment variables..."
    if [[ -z "${ADMIN_EMAIL}" ]] || [[ -z "${ADMIN_PSW}" ]]; then
            echo "ERROR: Environment variables not defined"
            echo " - Go to https://signup.conduktor.io and create an account for you"
            echo " - Export environment variables:"
            echo "     export ADMIN_EMAIL=<as setup on Conduktor>"
            echo "     export ADMIN_PSW=<as setup on Conduktor>"
            echo ""
            echo "Alternativelly, run '$0 -nc' to bypass the Conduktor platform demo"
            echo ""
            exit 1
    fi
fi
echo ""

echo "Starting up docker compose..."
docker compose up -d

echo ""
echo "Confluent Control Center:"
echo " - http://localhost:9021"
echo " - docs: https://docs.confluent.io/platform/current/control-center/index.html"
echo "Confluent REST Proxy:"
echo " - http://localhost:8082/v3/clusters"
echo " - docs: https://docs.confluent.io/platform/current/kafka-rest/api.html"
echo "Confluent ksqldb CLI:"
echo " - docker-compose exec ksqldb-cli bash -c 'ksql -u ksqlDBUser -p ksqlDBUser http://ksqldb-server:8088'"
echo " - docs: https://ksqldb.io/quickstart.html"
echo "Connect REST Proxy:"
echo " - http://localhost:8083"
echo " - docs: https://docs.confluent.io/platform/current/connect/references/restapi.html"
echo ""
sleep 1

echo "Kafka UI:"
echo " - http://localhost:8888"
echo " - docs: https://github.com/provectus/kafka-ui"
echo ""
sleep 1

echo "AKHQ:"
echo " - http://localhost:9000"
echo " - docs: https://akhq.io/docs"
echo ""
sleep 1

if [ $by_pass_conduktor -eq 0 ]; then
    echo "Conduktor platform:"
    echo " - http://localhost:8080 (user: admin@demo.dev | password: password)"
    echo " - docs: https://docs.conduktor.io/platform"
    echo ""
    sleep 1
fi

echo -n "Waiting for Kafka cluster to be ready..."
waiting_counter=0
while [ "$(curl -s -w '%{http_code}' -o /dev/null 'http://localhost:8082/v3/clusters')" -ne 200 ]; do
    echo -n "."
    sleep 2
    waiting_counter=$((waiting_counter+1))
    if [ $waiting_counter -eq 30 ]; then
        echo ""
        echo ""
        echo "ERROR: Unable to start the Kafka cluster!"
        echo ""
        sleep 1
        ./stop.sh
        echo ""
        exit 1
    fi
done
echo ""

echo ""
echo "Starting AVRO and Protobuf producers..."
sleep 3
ps aux | grep ' producer_avro.py'  | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
python3 producer_avro.py > /dev/null &
echo " - Started AVRO producer (topic: demo-avro)"

sleep 3
ps aux | grep ' producer_proto.py' | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
python3 producer_proto.py > /dev/null &
echo " - Started Protobuf producer (topic: demo-protobuf)"

echo ""
