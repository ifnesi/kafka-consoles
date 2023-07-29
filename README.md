# Kafka Consoles (this is still a work in progress)
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
- Two producers will be started:
  - AVRO:
    - Topic: demo-avro
  - Protobuf:
    - Topic: demo-protobuf
- Confluent Control Center: http://localhost:9021
- Kafka UI: http://localhost:8888
- Conduktor console:
  - Go to https://signup.conduktor.io and create an user for you
  - Create a YAML file as below
  ```
  organization:
     name: Home
  admin:
     email: <as per created on conduktor.io>
     password: <as per created on conduktor.io>
  ```
  - Upload the YAML file
  - http://localhost:8080


## Stop the demo
Run the script `./stop.sh` to stop the demo.