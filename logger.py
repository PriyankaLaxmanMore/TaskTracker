import logging
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from context import request_id_var

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# =====================
# JSON FORMATTER
# =====================
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": request_id_var.get(),
        }
        return json.dumps(log_record)


# =====================
# LOGGER SETUP
# =====================
def get_logger():
    logger = logging.getLogger("tasktracker")

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())

        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL.upper())

        logger.propagate = False

    return logger


logger = get_logger()
