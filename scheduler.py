from collections import deque

from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, timer, runnable, blocked, quantum=3):
        self.quantum = quantum
        self.timer = timer
        self.runnable = runnable
        self.blocked = blocked

    def scheduling(self, logs, inventory):
        def check_blocked_processes():
            if len(self.blocked) > 0 and len(inventory) > 0:
                temp(self.blocked.popleft(), Transition.BLOCKED_READY,
                     self.runnable.appendleft)

        def temp(process, transition, action=lambda p: ...):
            logs.append(Log(self.timer.now(), process, transition))
            action(process)
            process.state = transition.after()

        _timer = Timer()

        check_blocked_processes()
        temp(p := self.runnable.popleft(), Transition.READY_RUNNING)
        try:
            while p.state == State.RUNNING and next(_timer) < self.quantum:
                p.doWork()
                next(self.timer)
            if p.state == State.RUNNING:
                temp(p, Transition.RUNNING_READY, self.runnable.append)
            elif p.state == State.FINISHED:
                temp(p, Transition.RUNNING_FINISHED)
        except EmptyInventoryError:
            temp(p, Transition.RUNNING_BLOCKED, self.blocked.append)


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
