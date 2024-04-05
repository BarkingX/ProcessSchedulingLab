from functools import partial
from collections import deque

from simulation.process import Producer, Consumer
from simulation.scheduler import RoundRobinScheduler
from simulation.util import Timer, Log

if __name__ == '__main__':
    def log_transition(transition, process, timer):
        logs.append(Log(timer.now(), process, transition))

    def perform_transition(transition, process, action=lambda p: ...):
        action(process)
        process.state = transition.after()


    logs = []
    timer = Timer(1)
    inventory = []
    append = inventory.append
    pop = inventory.pop

    p = Producer(append)
    p.remaining_time = 3 * p.working_time_unit

    ps = deque([p, Consumer(pop), Consumer(pop), Producer(append)])
    bps = deque([])

    scheduler = RoundRobinScheduler(timer, ps, bps)

    while True and (len(ps) > 0 or len(bps) > 0):
        scheduler.scheduling(lambda: len(inventory) > 0, perform_transition,
                             partial(log_transition, timer=timer))

    # print(logs)
    for log in logs:
        print(log)
