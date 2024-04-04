from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, timer, runnable, blocked, quantum=3):
        self.quantum = quantum
        self.timer = timer
        self.runnable = runnable
        self.blocked = blocked

    def scheduling(self, logs, inventory_not_empty):
        def perform_transition(process, transition, action=lambda p: ...):
            log_transition(process, transition)
            action(process)
            process.state = transition.after()

        def log_transition(process, transition):
            logs.append(Log(self.timer.now(), process, transition))

        def unblock_if_possible():
            if len(self.blocked) > 0 and inventory_not_empty():
                perform_transition(self.blocked.popleft(), Transition.BLOCKED_READY,
                                   self.runnable.appendleft)

        _timer = Timer()

        unblock_if_possible()
        perform_transition(process := self.runnable.popleft(), Transition.READY_RUNNING)
        try:
            while process.state == State.RUNNING and next(_timer) < self.quantum:
                process.doWork()
                next(self.timer)
            if process.state == State.RUNNING:
                perform_transition(process, Transition.RUNNING_READY, self.runnable.append)
            elif process.state == State.FINISHED:
                perform_transition(process, Transition.RUNNING_FINISHED)
        except EmptyInventoryError:
            perform_transition(process, Transition.RUNNING_BLOCKED, self.blocked.append)


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
