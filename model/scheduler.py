import itertools
import math

from simulation.util import *
from functools import partial


def _log_transition(logs, time, trans, procs):
    logs.append(Log(time, trans, procs))


class RoundRobinScheduler:
    logs = []
    running = None
    elapsed_time = None

    def __init__(self, timer, model, quantum=3):
        self.timer = timer
        self.runnables = model.runnables
        self.blockeds = model.blockeds
        self.item_count = model.item_count
        self.quantum = quantum

    def scheduling(self):
        if not self.running:
            self._try_unblock_if_possible()
            self.elapsed_time = 0
            self.running = self.runnables.popleft()
            self._log_and_transition(Transition.READY_RUNNING, self.running)

        self._run_process(self.running)

        if not self.running.state == State.RUNNING:
            self.running = None

    def _try_unblock_if_possible(self):
        if len(self.blockeds) > 0 and self.item_count() > 0:
            self._log_and_transition(Transition.BLOCKED_READY,
                                     self.blockeds.popleft(),
                                     after_t=self.runnables.appendleft)

    def _log_and_transition(self, t, p, *, after_t=lambda p: ...):
        _log_transition(self.logs, self.timer.now(), t, p)
        p.state = t.after()
        after_t(p)

    def _run_process(self, p):
        try:
            if self.elapsed_time < self.quantum:
                p.run()
                self.timer.next()
                self.elapsed_time += 1
        except EmptyInventoryError:
            self._log_and_transition(Transition.RUNNING_BLOCKED, p,
                                     after_t=self.blockeds.append)
        else:
            if math.isclose(0, p.remaining_time):
                self._log_and_transition(Transition.RUNNING_FINISHED, p)
            elif self.elapsed_time >= self.quantum:
                self._log_and_transition(Transition.RUNNING_READY, p,
                                         after_t=self.runnables.append)


class Transition(Enum):
    RUNNING_BLOCKED = (State.RUNNING, State.BLOCKED, '库存不足')
    RUNNING_READY = (State.RUNNING, State.READY, '时间片到')
    READY_RUNNING = (State.READY, State.RUNNING, '调度运行')
    BLOCKED_READY = (State.BLOCKED, State.READY, '库存变化')
    RUNNING_FINISHED = (State.RUNNING, State.FINISHED, '任务完成')

    def __str__(self):
        return f'由“{self.value[0]:s}”到“{self.value[1]:s}”, {self.value[2]}'

    def after(self):
        return self.value[1]
