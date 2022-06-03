from datetime import datetime
import logging
import os
import inspect

LOGGER = logging.Logger("maxp")
LOGGER_FILENAME = os.path.join(os.getenv("temp"), "maxp.log")
LOGGER.addHandler(logging.FileHandler(LOGGER_FILENAME))


def log(msg: str, level: int = logging.INFO, indent: int = 0) -> None:
    # Get the execution stack and determine if we executed from a class
    # or from a standalone method.
    stack = inspect.stack()
    firstLayer = stack[1][0]
    if "self" in firstLayer.f_locals:
        name = firstLayer.f_locals["self"].__class__.__name__
    else:
        name = firstLayer.f_code.co_name

    # Current date/time
    now = f"[{datetime.now()}]"

    # The name of the entry
    name = f"[{name}]"

    # Calculate indent
    indent = " " * indent * 4 if indent > 0 else ""

    # Log to the file
    LOGGER.log(level, " ".join([now, name, indent, msg]))


def getLogFileName() -> str:
    return LOGGER_FILENAME
