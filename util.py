from enum import Enum

from simulation.strings import Strings


class State(Enum):
    READY = Strings.READY
    RUNNING = Strings.RUNNING
    BLOCKED = Strings.BLOCKED
    FINISHED = Strings.FINISHED
    INITIALED = '-'

    def __str__(self):
        return self.value


class Transition(Enum):
    INITIALIZED_READY = (State.INITIALED, State.READY, Strings.INITIALIZED_READY)
    RUNNING_BLOCKED = (State.RUNNING, State.BLOCKED, Strings.RUNNING_BLOCKED)
    RUNNING_READY = (State.RUNNING, State.READY, Strings.RUNNING_READY)
    READY_RUNNING = (State.READY, State.RUNNING, Strings.READY_RUNNING)
    BLOCKED_READY = (State.BLOCKED, State.READY, Strings.BLOCKED_READY)
    RUNNING_FINISHED = (State.RUNNING, State.FINISHED, Strings.RUNNING_FINISHED)

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
    def __init__(self, message=Strings.NO_RUNNABLE_PROCESS):
        super().__init__(message)


class Log:
    metadata = ('调度时间', '调度进程', '调度前状态', '调度后状态', '描述')

    def __init__(self, occur_time, process, transition):
        self.time = occur_time
        self.process = process
        self.transition = transition

    def __str__(self):
        return (f'{self.time}时 {self.process} '
                f'{self.transition}')

    def __repr__(self):
        return str(self)


class RoundRobinLogger:
    def __init__(self):
        self.logs = []

    def log(self, occur_time, process, transition):
        self.logs.append(Log(occur_time, process, transition))

    def clear(self):
        self.logs.clear()


class RoundRobinTimer:
    def __init__(self):
        self.time = 0
        self.elapsed = 0

    @property
    def now(self):
        return self.time

    def within(self, upper, lower=0):
        return lower <= self.elapsed < upper

    def reset(self):
        self.reset_time()
        self.reset_elapsed()

    def reset_time(self):
        self.time = 0

    def reset_elapsed(self):
        self.elapsed = 0

    def increment(self, by=1):
        self.increment_time(by=by)
        self.increment_elapsed(by=by)

    def increment_time(self, by=1):
        self.time += by

    def increment_elapsed(self, by=1):
        self.elapsed += by


class Item:
    pass
