# Kafka Consoles and CLI/REST API interfaces
Kafka Consoles to try out:
- [Confluent Control Center](https://docs.confluent.io/platform/current/control-center/index.html)
- [Kafka UI](https://github.com/provectus/kafka-ui)
- [Conduktor platform](https://docs.conduktor.io/platform/)

Additional interfaces available:
- [Confluent REST Proxy](https://docs.confluent.io/platform/current/kafka-rest/index.html)
- [Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html)
- [ksqlDB CLI](https://ksqldb.io/quickstart.html)

## Requirements:
- [Docker Desktop + Compose](https://www.docker.com/products/docker-desktop)
- [librdkafka](https://github.com/confluentinc/librdkafka) (`brew install librdkafka`)
- [curl](https://curl.se/) (`brew install curl`)
- [Python 3.8+](https://www.python.org/downloads/)
  - Install requirements (`python3 -m pip install -r requirements.txt`)

## Start the demo
This demo will run on [Confluent Platform](https://docs.confluent.io/platform/current/overview.html) version 7.4.1 (1x, Zookeeper, 1x Broker, REST Proxy, Schema Registry, Connect with DataGen source loaded and ksqlDB).

Run the script `./start.sh` to start the demo.
- Two producers will be instantiated:
  - `producer_avro.py` (AVRO): Producing to the topic `demo-avro`
    - Asset tracking device
    - Fields:
      - serial_number (string)
      - temperature (double)
      - humidity (double)
      - latitude (double)
      - longitude (double)
      - timestamp (long | timestamp-millis)
      - tampered (boolean)
  - `producer_proto.py` (Protobuf): Producing to the topic `demo-protobuf`
    - Purchase data
    - Fields:
      - item (string)
      - total_cost (double)
      - customer_id (string)
- Confluent Control Center: http://localhost:9021
- Kafka UI: http://localhost:8888
- Conduktor platform (sign-up required):
  - Go to https://signup.conduktor.io and create an account for you
  - Export environment variables:
    ```
    export ADMIN_EMAIL="<as setup on Conduktor>"
    export ADMIN_PSW="<as setup on Conduktor>"
    ```
  - Access the platform: http://localhost:8080 (user: `admin@demo.dev` | password: `password`)

Endpoints and interfaces access:
- Confluent Control Center:
  - http://localhost:9021
  - docs: https://docs.confluent.io/platform/current/control-center/index.html
- Confluent REST Proxy:
  - http://localhost:8082/v3/clusters
  - docs: https://docs.confluent.io/platform/current/kafka-rest/api.html
- Confluent ksqldb CLI:
  - ```docker-compose exec ksqldb-cli bash -c 'ksql -u ksqlDBUser -p ksqlDBUser http://ksqldb-server:8088'```
  - docs: https://ksqldb.io/quickstart.html
- Connect REST Proxy:
  - http://localhost:8083
  - docs: https://docs.confluent.io/platform/current/connect/references/restapi.html
- Kafka UI:
  - http://localhost:8888
  - docs: https://github.com/provectus/kafka-ui
- Conduktor platform:
  - http://localhost:8080 (user: admin@demo.dev | password: password)
  - docs: https://docs.conduktor.io/platform

## Stop the demo
Run the script `./stop.sh` to stop the demo.

# External References
- Confluent Control Center: https://docs.confluent.io/platform/current/control-center/index.html
- Kafka UI: https://github.com/provectus/kafka-ui
- Conduktor platform: https://docs.conduktor.io/platform/
- librdkafka (the Apache Kafka C/C++ client library): https://github.com/confluentinc/librdkafka

Check out [Confluent's Developer portal](https://developer.confluent.io), it has free courses, documents, articles, blogs, podcasts and so many more content to get you up and running with a fully managed Apache Kafka service.

Disclaimer: I work for Confluent :wink: