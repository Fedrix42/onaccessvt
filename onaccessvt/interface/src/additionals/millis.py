import time


def millis() -> int:
    """Return current time in milliseconds, useful for unblocking delays"""
    return round(time.time() * 1000)
