import itertools
from collections import deque

from simulation.model.process import Producer, Consumer
from simulation.model.scheduler import RoundRobinScheduler
from simulation.util import Timer

inventory = []
append = inventory.append
pop = inventory.pop
not_empty = lambda: len(inventory)

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


temp_model = Timer()
temp_model.runnables = ps
temp_model.blockeds = bps
temp_model.item_count = not_empty

scheduler = RoundRobinScheduler(Timer(1), temp_model)

while True and (len(ps) > 0 or len(bps) > 0 or scheduler.running):
    scheduler.scheduling()

for log in scheduler.logs:
    print(log)

