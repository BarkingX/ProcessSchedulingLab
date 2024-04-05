from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, timer, runnable, blocked, quantum=3):
        self.quantum = quantum
        self.timer = timer
        self.runnable = runnable
        self.blocked = blocked

    def scheduling(self, inventory_not_empty, transition, log):
        def log_and_transition(t, p, *args):
            log(t, p)
            transition(t, p, *args)

        def unblock_if_possible():
            if len(self.blocked) > 0 and inventory_not_empty():
                log_and_transition(Transition.BLOCKED_READY, self.blocked.popleft(),
                                   self.runnable.appendleft)

        def run(p):
            _timer = Timer()
            try:
                while p.state == State.RUNNING and next(_timer) < self.quantum:
                    p.run()
                    next(self.timer)
            except EmptyInventoryError:
                log_and_transition(Transition.RUNNING_BLOCKED, p,
                                   self.blocked.append)
            else:
                if p.state == State.FINISHED:
                    log_and_transition(Transition.RUNNING_FINISHED, p)
                else:
                    log_and_transition(Transition.RUNNING_READY, p,
                                       self.runnable.append)

        unblock_if_possible()
        process = self.runnable.popleft()
        log_and_transition(Transition.READY_RUNNING, process)
        run(process)


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
