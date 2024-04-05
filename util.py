import itertools
from enum import Enum


class State(Enum):
    READY = '就绪'
    RUNNING = '运行'
    BLOCKED = '等待'
    FINISHED = '完成'

    def __str__(self):
        return self.value


class EmptyInventoryError(Exception):
    def __init__(self, message="库存为空"):
        super().__init__(message)


class SchedulerService:
    logs = []

    def __init__(self, timer, inventory_not_empty):
        self.timer = timer
        self.inventory_not_empty = inventory_not_empty

    def log_transition(self, transition, process):
        self.logs.append(Log(self.timer.now(), transition, process))

    @staticmethod
    def perform_transition(transition, process, action=lambda p: ...):
        process.state = transition.after()
        action(process)


class Timer(itertools.count):
    _now = 0

    def __next__(self):
        self._now = super().__next__()
        return self._now

    def now(self):
        return self._now

    def next(self):
        return self.__next__()


class Log:
    def __init__(self, occur_time, transition, process):
        self.time = occur_time
        self.process = process
        self.transition = transition

    def __str__(self):
        return (f'{self.time}时 {self.process} '
                f'{self.transition}')

    def __repr__(self):
        return str(self)


class Item:
    pass


