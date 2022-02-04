import time

from typing import List, Optional
from queue import Queue


class broroutine:
    active: Optional[bool] = None

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class Loop:
    current_threads: List[broroutine]
    promises: Queue

    def __init__(self):
        self.current_threads = []
        self.promises = Queue()
        self.waiting = []

    def run(self, task: broroutine):
        return self.queue.put(task)

    def check_current_thread(self):
        if self.empty:
            pass

    @property
    def empty(self) -> bool:
        """Returns whether or not"""
        return len(self.current_threads) == 0



