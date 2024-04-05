import itertools
import math
from time import sleep

from simulation.util import State, EmptyInventoryError, Item


class Process:
    _id_generator = itertools.count(1)
    working_time_unit = .5

    def __init__(self):
        self.id = next(self._id_generator)
        self.state = State.READY
        self.remaining_time = 5 * self.working_time_unit

    def run(self):
        sleep(self.working_time_unit)
        self.remaining_time -= self.working_time_unit
        if math.isclose(self.remaining_time, 0):
            self.state = State.FINISHED

    def __str__(self):
        return f'进程{self.id}:{self.__class__.__name__}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, state={self.state})'


class Producer(Process):
    def __init__(self, append_item):
        super().__init__()
        self.append_item = append_item

    def run(self):
        super().run()
        if self.state == State.FINISHED:
            self.append_item(Item())


class Consumer(Process):
    def __init__(self, get_item):
        super().__init__()
        self.get_item = get_item
        self.item = None

    def run(self):
        try:
            self.item = self.item or self.get_item()
        except IndexError as e:
            raise EmptyInventoryError(e)
        super().run()
