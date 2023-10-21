import json
import logging
from logging import Formatter
import os

def create_log_dir():
    try:
        if not os.path.exists("logs"):
            os.makedirs("logs")
    except OSError:
        raise ("Error: Failed to create the log directory.")


class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()
    def format(self, record):
        json_record = {}
        json_record["message"] = record.getMessage()
        if "timestamp" in record.__dict__:
            json_record["timestamp"] = record.__dict__["timestamp"]
        if "req" in record.__dict__:
            json_record["req"] = record.__dict__["req"]
        if "res" in record.__dict__:
            json_record["res"] = record.__dict__["res"]
        if record.levelno == logging.ERROR and record.exc_info:
            json_record["err"] = self.formatException(record.exc_info)
        return json.dumps(json_record)

logger = logging.root



create_log_dir()
handler = logging.FileHandler('logs/output.log')
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(logging.DEBUG)

logging.getLogger("uvicorn.access").disabled = True