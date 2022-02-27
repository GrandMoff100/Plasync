import time
from dataclasses import dataclass
from typing import Generator, Optional


@dataclass()
class Task:
    coro: Generator
    loop: "EventLoop"
    waiting_until: Optional[float] = None

    @property
    def active(self) -> bool:
        return self.loop.active_task is self


class EventLoop:
    active_task: Optional[Task] = None
    active_loop: Optional["EventLoop"] = None 

    def __init__(self):
        self.queue = []

    def promise(self, coro):
        self.queue.append(Task(coro, loop=self))
    
    def run(self):
        EventLoop.active_loop = self
        while self.queue:
            self.active_task = None
            if task := self.get_next_task():
                try:
                    self.active_task = task
                    next(task.coro)
                except StopIteration as exc:
                    continue
                self.queue.append(task)

    def get_next_task(self) -> Optional[Task]:
        for i, task in enumerate(self.queue):
            if not task.active:
                if task.waiting_until is not None:
                    if task.waiting_until <= time.time():
                        self.queue.pop(i)
                        return task
                    return None
                self.queue.pop(i)
                return task
        return None


def sleep(seconds: float):
    if loop := EventLoop.active_loop:
        loop.active_task.waiting_until = time.time() + seconds
    else:
        raise NoActiveLoopError("Lol you need an active loop in order to sleep.")
    yield