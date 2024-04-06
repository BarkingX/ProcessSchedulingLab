from collections import deque

from simulation.model.process import Producer, Consumer, Process
from simulation.model.scheduler import RoundRobinScheduler, ScheduleHelper
from simulation.util import Timer


class SimulationModel:
    def __init__(self):
        self.inventory = []
        self.processes = []
        self.runnable = deque()
        self.blocked = deque()
        self.timer = Timer(1)
        self.helper = ScheduleHelper(self.timer, lambda: len(self.inventory) > 0)
        self.scheduler = RoundRobinScheduler(self.runnable, self.blocked, self.helper)

    def add_type(self, process_type, **kwargs):
        if 'Producer' == process_type:
            self.add_producer(**kwargs)
        elif 'Consumer' == process_type:
            self.add_consumer(**kwargs)

    def add_producer(self, **kwargs):
        self.add_process(self.new_producer(**kwargs))

    def add_consumer(self, **kwargs):
        self.add_process(self.new_consumer(**kwargs))

    def add_process(self, process):
        self.processes.append(process)
        self.runnable.append(process)

    def new_type(self, process_type, **kwargs):
        if 'Producer' == process_type:
            return self.new_producer(**kwargs)
        elif 'Consumer' == process_type:
            return self.new_consumer(**kwargs)

    def new_producer(self, **kwargs):
        return Producer(self.inventory.append, **kwargs)

    def new_consumer(self, **kwargs):
        return Consumer(self.inventory.pop, **kwargs)

