from loguru import logger
import json

def __serialize(record):
    subset = {"level": record["level"].name.lower(), "ts": record["time"].timestamp(), "msg": record["message"], **record["extra"]}
    return json.dumps(subset)

def __sink(message):
    print(__serialize(message.record))

def init_logger():
    logger.remove()
    logger.add(__sink)
