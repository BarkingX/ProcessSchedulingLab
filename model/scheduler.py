import math

from simulation.model.process import Process
from simulation.util import *
from simulation.util import Transition


def _log_transition(logs, time, trans, procs):
    logs.append(Log(time, trans, procs))


class RoundRobinScheduler:
    dummy_process = Process(0)
    dummy_process.id = None

    def __init__(self, model, quantum=3):
        self.runnables = model.runnables
        self.blockeds = model.blockeds
        self.item_count = model.item_count
        self.quantum = quantum
        self._init()
        self._logs = []


    def _init(self):
        self.running = None
        self._elapsed_time = 0
        self._timer = Timer(1)

    def reset(self):
        self._init()
        self._logs.clear()

    def scheduling(self):
        if not self.running:
            self._elapsed_time = 0
            self._try_unblock_if_possible()
            if len(self.runnables) == 0:
                raise NoRunnableProcessesError()
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
        _log_transition(self._logs, self._timer.now(), t, p)
        p.state = t.after()
        after_t(p)

    def _run_process(self, p):
        try:
            if self._elapsed_time < self.quantum:
                p.run()
                next(self._timer)
                self._elapsed_time += 1
        except EmptyInventoryError:
            self._log_and_transition(Transition.RUNNING_BLOCKED, p,
                                     after_t=self.blockeds.append)
        else:
            if math.isclose(0, p.remaining_time):
                self._log_and_transition(Transition.RUNNING_FINISHED, p)
            elif self._elapsed_time >= self.quantum:
                self._log_and_transition(Transition.RUNNING_READY, p,
                                         after_t=self.runnables.append)

    def now(self):
        return self._timer.now()

    def logs(self):
        return self._logs
