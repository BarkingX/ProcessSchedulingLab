from collections import deque

from simulation.process import Producer, Consumer
from simulation.scheduler import RoundRobinScheduler
from simulation.util import Timer, SchedulerService


inventory = []
append = inventory.append
pop = inventory.pop
not_empty = lambda: len(inventory) > 0

p = Producer(append)
p.remaining_time = 3 * p.working_time_unit

ps = deque([p, Consumer(pop)])
bps = deque()


def add_new_producer():
    ps.append(Producer(append))


def add_new_consumer():
    ps.append(Consumer(pop))


add_new_consumer()
add_new_producer()

service = SchedulerService(Timer(1), not_empty)
scheduler = RoundRobinScheduler(ps, bps, service)

while True and (len(ps) > 0 or len(bps) > 0):
    scheduler.scheduling()

for log in service.logs:
    print(log)
