import threading
import logging
import time
import os


SLEEP_TIME = float(os.environ.get("SLEEP_TIME", 0))
METRICS_TAGS = {"foo": "bar"}


class Model:
    def __init__(self):
        logging.info(f"Test secret: {os.environ.get('TEST_MOCK_SECRET', None)}")

    def predict(self, features, names=None, meta=None):

        logging.info(f"My id is {id(self)}")
        logging.info(f"OS pid is {os.getpid()}")
        logging.info(f"OS thread is {threading.current_thread().name}")

        if SLEEP_TIME > 0:
            logging.info(f"Sleeping for {SLEEP_TIME} seconds")
            time.sleep(SLEEP_TIME)

        logging.info(f"model features: {features}")
        logging.info(f"model names: {names}")
        logging.info(f"model meta: {meta}")
        return features

    def tags(self):
        return {"tag a": "a", "tag b": "b"}

    def metrics(self):
        return [
            {"type": "COUNTER", "key": "mycounter", "value": 1, "tags": METRICS_TAGS},
            {"type": "GAUGE", "key": "mygauge", "value": 100, "tags": METRICS_TAGS},
            {"type": "TIMER", "key": "mytimer", "value": 20.2, "tags": METRICS_TAGS},
        ]
