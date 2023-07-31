import sys
import time
import random
import argparse
import datetime
import platform

from pydantic import BaseModel
from confluent_kafka import Producer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


# Global variables
SERIAL_NUMBER = [f"atrk_{i:02d}" for i in range(1, 26)]


class AssetTracking(BaseModel):
    serial_number: str
    temperature: float
    humidity: float
    latitude: float
    longitude: float
    timestamp: int
    tampered: bool


def genRandom(ndigits: int = 2) -> float:
    return (
        (-1 if random.random() > 0.5 else 1)
        * int(random.random() * 10**ndigits)
        / 10**ndigits
    )


def dataDict(
    data: AssetTracking,
    ctx,
) -> dict:
    """
    Returns a dict representation of a data instance for serialization.
    Args:
        data (AssetTracking): AssetTracking instance.
        ctx (SerializationContext): Metadata pertaining to the serialization
            operation.
    Returns:
        dict: Dict populated with user attributes to be serialized.
    """
    return dict(data)


def deliveryReport(err, msg):
    """
    Reports the failure or success of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """

    if err is not None:
        print(f"Delivery failed for Data record {msg.key()}: {err}", file=sys.stderr)
        return
    print(
        f"Data record {msg.key().decode('utf-8')} successfully produced to {msg.topic()}:{msg.partition()} at offset {msg.offset()}"
    )


def main(args):
    with open(f"avro/{args.topic}.avsc") as f:
        schema_str = f.read()

    schema_registry_conf = {
        "url": args.schema_registry,
    }
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    avro_serializer = AvroSerializer(
        schema_registry_client,
        schema_str,
        dataDict,
    )

    producer_conf = {
        "bootstrap.servers": args.bootstrap_servers,
    }

    print(f"Producing records to topic '{args.topic}'. ^C to exit.")

    producer = Producer(producer_conf)
    initial_data = dict()
    while True:
        # Serve on_delivery callbacks from previous calls to produce()
        producer.poll(0.0)
        try:
            serial_numer = random.choice(SERIAL_NUMBER)
            if initial_data.get(serial_numer) is None:
                initial_data[serial_numer] = {
                    "temperature": int(random.randint(-2000, 4500)) / 100,
                    "humidity": int(random.randint(0, 10000)) / 100,
                    "latitude": int(random.randint(-900000, 900000)) / 10000,
                    "longitude": int(random.randint(-1800000, 1800000)) / 10000,
                }
            else:
                initial_data[serial_numer]["temperature"] += genRandom()
                initial_data[serial_numer]["humidity"] = min(
                    100, initial_data[serial_numer]["humidity"] + genRandom()
                )
                initial_data[serial_numer]["latitude"] = max(
                    -90,
                    min(
                        90,
                        initial_data[serial_numer]["latitude"] + genRandom(6),
                    ),
                )
                initial_data[serial_numer]["longitude"] = max(
                    -180,
                    min(
                        180,
                        initial_data[serial_numer]["longitude"] + genRandom(6),
                    ),
                )

            data = AssetTracking(
                serial_number=serial_numer,
                temperature=initial_data[serial_numer]["temperature"],
                humidity=initial_data[serial_numer]["humidity"],
                latitude=initial_data[serial_numer]["latitude"],
                longitude=initial_data[serial_numer]["longitude"],
                timestamp=int(datetime.datetime.utcnow().timestamp() * 1000),
                tampered=(random.random() > 0.9),
            )
            producer.produce(
                topic=args.topic,
                headers={
                    "program": "python",
                    "version": platform.python_version(),
                    "node": platform.node(),
                    "environment": "test",
                },
                key=serial_numer,
                value=avro_serializer(
                    data,
                    SerializationContext(
                        args.topic,
                        MessageField.VALUE,
                    ),
                ),
                on_delivery=deliveryReport,
            )
        except KeyboardInterrupt:
            print("CTRL-C pressed by user", file=sys.stderr)
            break

        except ValueError as err_1:
            print(f"Invalid input, discarding record: {err_1}", file=sys.stderr)

        except Exception as err_2:
            print(f"Generic error: {err_2}", file=sys.stderr)

        time.sleep(0.5)

    print("\nFlushing records...")
    producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AvroSerializer example")
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
        default="demo-avro",
        help="Topic name",
    )

    main(parser.parse_args())
