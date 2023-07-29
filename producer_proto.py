# brew install protobuf
# protoc -I=. --python_out=. ./proto/Purchase.proto

import time
import uuid
import random
import argparse
import platform

from confluent_kafka import Producer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer

from proto import Purchase_pb2 as Purchase


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print(f"Delivery failed for User record {msg.key()}: {err}")
    else:
        print(
            f"User record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


def main(args):
    schema_registry_conf = {
        "url": args.schema_registry,
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    protobuf_serializer = ProtobufSerializer(
        Purchase.Purchase,
        schema_registry_client,
        {
            "use.deprecated.format": False,
        },
    )

    producer_conf = {
        "bootstrap.servers": args.bootstrap_servers,
    }
    producer = Producer(producer_conf)

    topic = args.topic
    print(f"Producing records to topic '{args.topic}'. ^C to exit.")

    while True:
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:
            purchase = Purchase.Purchase(
                item=uuid.uuid4().hex,
                total_cost=random.randint(0, 99999) / 100,
                customer_id=uuid.uuid4().hex,
            )
            producer.produce(
                topic=topic,
                headers={
                    "program": "python",
                    "version": platform.python_version(),
                    "node": platform.node(),
                    "environment": "test",
                },
                key=uuid.uuid4().hex,
                value=protobuf_serializer(
                    purchase,
                    SerializationContext(topic, MessageField.VALUE),
                ),
                on_delivery=delivery_report,
            )

        except (KeyboardInterrupt, EOFError):
            print("^C pressed by user")
            break

        except ValueError as err:
            print(f"Invalid input, discarding record: {err}")
            continue

        finally:
            time.sleep(0.5)

    print("\nFlushing records...")
    producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ProtobufSerializer example")
    parser.add_argument(
        "-b",
        dest="bootstrap_servers",
        default="localhost:9092",
        help="Bootstrap broker(s) (host[:port])",
    )
    parser.add_argument(
        "-s",
        dest="schema_registry",
        default="http://localhost:8081",
        help="Schema Registry (http(s)://host[:port]",
    )
    parser.add_argument(
        "-t",
        dest="topic",
        default="demo-protobuf",
        help="Topic name",
    )

    main(parser.parse_args())
