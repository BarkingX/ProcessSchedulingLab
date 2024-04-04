import itertools
import math
from time import sleep

from simulation.util import State, EmptyInventoryError, Item


class Process:
    _id_generator = itertools.count(1)

    def __init__(self):
        self.id = next(self._id_generator)
        self.state = State.READY
        self.working_time_unit = .5
        self.remaining_time = 5 * self.working_time_unit

    def doWork(self):
        pass

    def __str__(self):
        return f'进程{self.id}:{self.__class__.__name__}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, state={self.state})'


class Producer(Process):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def doWork(self):
        sleep(self.working_time_unit)
        self.remaining_time -= self.working_time_unit

        if math.isclose(self.remaining_time, 0):
            self.state = State.FINISHED
            self.items.append(Item())


class Consumer(Process):
    def __init__(self, items):
        super().__init__()
        self.items = items

    def doWork(self):
        if len(self.items) == 0:
            raise EmptyInventoryError()
        sleep(self.working_time_unit)
        self.remaining_time -= self.working_time_unit

        if math.isclose(self.remaining_time, 0):
            self.state = State.FINISHED
            self.items.pop()
