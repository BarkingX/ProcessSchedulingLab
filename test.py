from collections import deque

from simulation.model.process import Producer, Consumer
from simulation.model.scheduler import RoundRobinScheduler, ScheduleHelper
from simulation.util import Timer

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

helper = ScheduleHelper(Timer(1), not_empty)
scheduler = RoundRobinScheduler(ps, bps, helper)

while True and (len(ps) > 0 or len(bps) > 0):
    scheduler.scheduling()

for log in helper.logs:
    print(log)
