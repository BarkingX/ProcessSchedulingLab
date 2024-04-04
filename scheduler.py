from simulation.util import *
from simulation.util import State


class RoundRobinScheduler:
    def __init__(self, timer, runnable, blocked, quantum=3):
        self.quantum = quantum
        self.timer = timer
        self.runnable = runnable
        self.blocked = blocked

    def scheduling(self, logs, inventory):
        def next_process():
            if len(self.blocked) > 0 and len(inventory) > 0:
                p = self.blocked.popleft()

                temp(p, Transition.BLOCKED_READY, self.runnable.appendleft)

                # p.state = State.READY
                # self.runnable.appendleft(p)
                # logs.append(l := Log(self.timer.now(), p, Transition.BLOCKED_READY))

                # print(l)

            if len(self.runnable) > 0:
                return self.runnable.popleft()

        def temp(process, transition, action=lambda p: ...):
            logs.append(Log(self.timer.now(), process, transition))
            action(process)
            process.state = transition.after()

        _timer = Timer()
        p = next_process()

        temp(p, Transition.READY_RUNNING)

        # p.state = State.RUNNING
        # logs.append(l := Log(self.timer.now(), p, Transition.READY_RUNNING))

        # print(l)
        try:
            while p.state == State.RUNNING and next(_timer) < self.quantum:
                p.doWork()
                next(self.timer)
            if p.state == State.RUNNING:
                temp(p, Transition.RUNNING_READY, self.runnable.append)

                # p.state = State.READY
                # self.runnable.append(p)
                # logs.append(l := Log(self.timer.now(), p, Transition.RUNNING_READY))
                # print(l)
            elif p.state == State.FINISHED:
                logs.append(l := Log(self.timer.now(), p, Transition.RUNNING_FINISHED))
                # print(l)
        except EmptyInventoryError:

            p.state = State.BLOCKED
            self.blocked.append(p)
            logs.append(l := Log(self.timer.now(), p, Transition.RUNNING_BLOCKED))
            # print(l)


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

    @classmethod
    def of(cls, before, after):
        for transition in cls:
            if transition.value[:2] == (before, after):
                return transition
        raise ValueError(f"No such transition from {before} to {after}")