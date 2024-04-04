from collections import deque

from simulation.process import Producer, Consumer
from simulation.scheduler import RoundRobinScheduler
from simulation.util import Timer

if __name__ == '__main__':
    logs = []
    inventory = []
    timer = Timer(1)

    p = Producer(inventory)
    p.remaining_time = 3 * p.working_time_unit

    ps = deque([p, Consumer(inventory), Consumer(inventory), Producer(inventory)])
    bps = deque([])

    scheduler = RoundRobinScheduler(timer, ps, bps)

    while True and (len(ps) > 0 or len(bps) > 0):
        scheduler.scheduling(logs, lambda: len(inventory) > 0)

    # print(logs)
    for log in logs:
        print(log)
