import itertools
import re
from enum import Enum

from simulation.strings import Strings

valid_floats = re.compile(r'\d+(?:\.\d+)?')


def is_valid_floatnumber(s):
    return valid_floats.fullmatch(s)


class State(Enum):
    READY = Strings.READY
    RUNNING = Strings.RUNNING
    BLOCKED = Strings.BLOCKED
    FINISHED = Strings.FINISHED

    def __str__(self):
        return self.value


class Transition(Enum):
    RUNNING_BLOCKED = (State.RUNNING, State.BLOCKED, '库存不足')
    RUNNING_READY = (State.RUNNING, State.READY, '时间片到')
    READY_RUNNING = (State.READY, State.RUNNING, '调度运行')
    BLOCKED_READY = (State.BLOCKED, State.READY, '库存变化')
    RUNNING_FINISHED = (State.RUNNING, State.FINISHED, '任务完成')

    def __str__(self):
        return f'由“{self.before():s}”到“{self.after():s}”: {self.description()}'

    def before(self):
        return self.value[0]

    def after(self):
        return self.value[1]

    def description(self):
        return self.value[2]


class EmptyInventoryError(Exception):
    def __init__(self, message=Strings.EMPTY_INVENTORY):
        super().__init__(message)


class NoRunnableProcessesError(Exception):
    """Exception raised when no processes are runnable."""
    def __init__(self, message=Strings.NO_RUNNABLE_PROCESS):
        super().__init__(message)


class Timer(itertools.count):
    _now = 0

    def __next__(self):
        self._now = super().__next__()
        return self._now

    def now(self):
        return self._now




class Log:
    metadata = ('调度时间', '调度进程', '调度前状态', '调度后状态', '描述')

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
