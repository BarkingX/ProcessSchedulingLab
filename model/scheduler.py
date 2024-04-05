from simulation.util import *


class ScheduleHelper:
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


class RoundRobinScheduler:
    def __init__(self, runnable, blocked, helper: ScheduleHelper, quantum=3):
        self.runnable = runnable
        self.blocked = blocked
        self.helper = helper
        self.quantum = quantum

    def scheduling(self):
        self._unblock_if(len(self.blocked) > 0 and self.helper.inventory_not_empty())
        self._log_and_transition(Transition.READY_RUNNING, self.runnable.popleft(),
                                 after_t=self._run)

    def _unblock_if(self, condition):
        if condition:
            self._log_and_transition(Transition.BLOCKED_READY, self.blocked.popleft(),
                                     after_t=self.runnable.appendleft)

    def _log_and_transition(self, t, p, *, after_t=lambda p: ...):
        self.helper.log_transition(t, p)
        self.helper.perform_transition(t, p, after_t)

    def _run(self, p):
        _timer = Timer()
        try:
            while p.state == State.RUNNING and _timer.next() < self.quantum:
                p.run()
                self.helper.timer.next()
        except EmptyInventoryError:
            self._log_and_transition(Transition.RUNNING_BLOCKED, p,
                                     after_t=self.blocked.append)
        else:
            if p.state == State.FINISHED:
                self._log_and_transition(Transition.RUNNING_FINISHED, p)
            else:
                self._log_and_transition(Transition.RUNNING_READY, p,
                                         after_t=self.runnable.append)


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
