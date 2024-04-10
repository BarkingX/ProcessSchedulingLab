from simulation.util import *
from functools import partial

class RoundRobinScheduler:
    logs = []

    def __init__(self, timer, model, quantum=3):
        self.timer = timer
        self.runnable = model.runnable
        self.blocked = model.blocked
        self.item_count = model.item_count
        self.quantum = quantum

    def scheduling(self, *, after_every_run=None):
        self._try_unblock_if_possible()
        self._pop_next_runnable_to_run(after_every_run=after_every_run)

    def _try_unblock_if_possible(self):
        if len(self.blocked) > 0 and self.item_count() > 0:
            self._log_and_transition(Transition.BLOCKED_READY,
                                     self.blocked.popleft(),
                                     after_t=self.runnable.appendleft)

    def _log_and_transition(self, t, p, *, after_t=lambda p: ...):
        self.perform_transition(t, p, after_t)
        self.log_transition(t, p)

    def _pop_next_runnable_to_run(self, *, after_every_run=None):
        try:
            self._log_and_transition(Transition.READY_RUNNING,
                                     self.runnable.popleft(),
                                     after_t=partial(self._run,
                                                     after_every_run=after_every_run))
        except IndexError:
            pass

    def _run(self, p, *, after_every_run=None):
        _timer = Timer()
        try:
            while p.state == State.RUNNING and _timer.next() < self.quantum:
                if after_every_run:
                    after_every_run(p)
                p.run()
                self.timer.next()
        except EmptyInventoryError:
            self._log_and_transition(Transition.RUNNING_BLOCKED, p,
                                     after_t=self.blocked.append)
        else:
            if p.state == State.FINISHED:
                self._log_and_transition(Transition.RUNNING_FINISHED, p)
            elif p.state == State.RUNNING:
                self._log_and_transition(Transition.RUNNING_READY, p,
                                         after_t=self.runnable.append)
        finally:
            if after_every_run:
                after_every_run(p)

    def log_transition(self, transition, process):
        self.logs.append(Log(self.timer.now(), transition, process))

    @staticmethod
    def perform_transition(transition, process, action=lambda p: ...):
        process.state = transition.after()
        action(process)


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
