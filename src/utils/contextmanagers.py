# Standard Library
import signal
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def time_limit(seconds: int) -> Generator[None, None, None]:
    def signal_handler(signum, frame) -> None:
        raise TimeoutError

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
