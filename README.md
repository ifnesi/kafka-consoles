# Kafka Consoles
Try out three Kafka Consoles:
- [Confluent Control Center](https://docs.confluent.io/platform/current/control-center/index.html)
- [Kafka UI](https://github.com/provectus/kafka-ui)
- [Conduktor console](https://docs.conduktor.io/platform/console/)


## Requirements:
- Docker Desktop
- librdkafka (`brew install librdkafka`)
- Python 3.8+
- Install python requirements (`python3 -m pip install -r requirements.txt`)

## Start the demo
Run the script `./start.sh` to start the demo.
- Two producers will be instantiated:
  - `producer_avro.py`: Producing to the topic `demo-avro`
  - `producer_proto.py`: Producing to the topic `demo-protobuf`
- Confluent Control Center (already setup): http://localhost:9021
- Kafka UI (already setup): http://localhost:8888
- Conduktor console (setup required):
  - Go to https://signup.conduktor.io and create an user for you
  - Create a YAML file as shown below and have it saved locally:
  ```
  organization:
     name: Home
  admin:
     email: <as per created on conduktor.io>
     password: <as per created on conduktor.io>
  ```
  - Access the console: http://localhost:8080
  - Upload the YAML file (option `Upload YAML`) and sign-in
  - Endpoints (for when setting up your Kafka cluster on the console)):
    - Kafka Broker: broker:9094 (auth None)
    - Kafka connect: http://connect:8083 (no security)
    - Schema Registry: http://schema-registry:8081 (no security)


## Stop the demo
Run the script `./stop.sh` to stop the demo.