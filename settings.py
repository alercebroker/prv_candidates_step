import os
from fastavro import schema

##################################################
#       prv_candidates_step   Settings File
##################################################


def settings_creator():
    ## Set the global logging level to debug
    LOGGING_DEBUG = False

    ## Consumer configuration
    ### Each consumer has different parameters and can be found in the documentation
    CONSUMER_CONFIG = {
        "CLASS": "apf.consumers.KafkaConsumer",
        "PARAMS": {
            "bootstrap.servers": os.environ["CONSUMER_SERVER"],
            "group.id": os.environ["CONSUMER_GROUP_ID"],
            "auto.offset.reset": "beginning",
            "enable.partition.eof": True
            if os.getenv("ENABLE_PARTITION_EOF")
            else False,
        },
        "TOPICS": os.environ["CONSUMER_TOPICS"].split(","),
        "consume.messages": int(os.getenv("CONSUME_MESSAGES", "1")),
        "consume.timeout": int(os.getenv("CONSUME_TIMEOUT", "10")),
    }

    PRODUCER_CONFIG = {
        "CLASS": "apf.producers.KafkaProducer",
        "PARAMS": {
            "bootstrap.servers": os.environ["PRODUCER_SERVER"],
        },
        "TOPIC": os.environ["PRODUCER_TOPIC"],
        "SCHEMA": schema.load_schema("schema.avsc"),
    }

    SCRIBE_PRODUCER_CONFIG = {
        "CLASS": os.getenv("SCRIBE_PRODUCER_CLASS", "apf.producers.KafkaProducer"),
        "PARAMS": {
            "bootstrap.servers": os.environ["PRODUCER_SERVER"],
        },
        "TOPIC": os.environ["SCRIBE_PRODUCER_TOPIC"],
        "SCHEMA": schema.load_schema("scribe_schema.avsc"),
    }

    METRICS_CONFIG = {
        "CLASS": os.getenv("METRICS_CLASS", "apf.metrics.KafkaMetricsProducer"),
        "EXTRA_METRICS": [
            {"key": "candid", "format": lambda x: str(x)},
        ],
        "PARAMS": {
            "PARAMS": {
                "bootstrap.servers": os.getenv("METRICS_HOST"),
                "auto.offset.reset": "smallest",
            },
            "TOPIC": os.getenv("METRICS_TOPIC", "metrics"),
            "SCHEMA": {
                "$schema": "http://json-schema.org/draft-07/schema",
                "$id": "http://example.com/example.json",
                "type": "object",
                "title": "The root schema",
                "description": "The root schema comprises the entire JSON document.",
                "default": {},
                "examples": [
                    {"timestamp_sent": "2020-09-01", "timestamp_received": "2020-09-01"}
                ],
                "required": ["timestamp_sent", "timestamp_received"],
                "properties": {
                    "timestamp_sent": {
                        "$id": "#/properties/timestamp_sent",
                        "type": "string",
                        "title": "The timestamp_sent schema",
                        "description": "Timestamp sent refers to the time at which a message is sent.",
                        "default": "",
                        "examples": ["2020-09-01"],
                    },
                    "timestamp_received": {
                        "$id": "#/properties/timestamp_received",
                        "type": "string",
                        "title": "The timestamp_received schema",
                        "description": "Timestamp received refers to the time at which a message is received.",
                        "default": "",
                        "examples": ["2020-09-01"],
                    },
                },
                "additionalProperties": True,
            },
        },
    }

    if os.getenv("KAFKA_USERNAME") and os.getenv("KAFKA_PASSWORD"):
        CONSUMER_CONFIG["PARAMS"]["security.protocol"] = "SASL_SSL"
        CONSUMER_CONFIG["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        CONSUMER_CONFIG["PARAMS"]["sasl.username"] = os.getenv("KAFKA_USERNAME")
        CONSUMER_CONFIG["PARAMS"]["sasl.password"] = os.getenv("KAFKA_PASSWORD")
        PRODUCER_CONFIG["PARAMS"]["security.protocol"] = "SASL_SSL"
        PRODUCER_CONFIG["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        PRODUCER_CONFIG["PARAMS"]["sasl.username"] = os.getenv("KAFKA_USERNAME")
        PRODUCER_CONFIG["PARAMS"]["sasl.password"] = os.getenv("KAFKA_PASSWORD")
        SCRIBE_PRODUCER_CONFIG["PARAMS"]["security.protocol"] = "SASL_SSL"
        SCRIBE_PRODUCER_CONFIG["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        SCRIBE_PRODUCER_CONFIG["PARAMS"]["sasl.username"] = os.getenv("KAFKA_USERNAME")
        SCRIBE_PRODUCER_CONFIG["PARAMS"]["sasl.password"] = os.getenv("KAFKA_PASSWORD")
        METRICS_CONFIG["PARAMS"]["PARAMS"]["security.protocol"] = "SASL_SSL"
        METRICS_CONFIG["PARAMS"]["PARAMS"]["sasl.mechanism"] = "SCRAM-SHA-512"
        METRICS_CONFIG["PARAMS"]["PARAMS"]["sasl.username"] = os.getenv(
            "KAFKA_USERNAME"
        )
        METRICS_CONFIG["PARAMS"]["PARAMS"]["sasl.password"] = os.getenv(
            "KAFKA_PASSWORD"
        )

    ## Step Configuration
    STEP_CONFIG = {
        "CONSUMER_CONFIG": CONSUMER_CONFIG,
        "METRICS_CONFIG": METRICS_CONFIG,
        "PRODUCER_CONFIG": PRODUCER_CONFIG,
        "SCRIBE_PRODUCER_CONFIG": SCRIBE_PRODUCER_CONFIG,
        "LOGGING_DEBUG": LOGGING_DEBUG,
    }
    return STEP_CONFIG
