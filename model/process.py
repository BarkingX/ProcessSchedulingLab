import itertools
import math

from simulation import strings
from simulation.util import State, EmptyInventoryError, Item


class Process:
    _id_generator = itertools.count(1)
    working_time_unit = 1
    default_burst_time = 5 * working_time_unit

    def __init__(self, burst_time=default_burst_time):
        self.id = next(self._id_generator)
        self.state = State.READY
        self.remaining_time = burst_time

    def run(self):
        # TODO
        # sleep(self.working_time_unit)
        self.remaining_time -= self.working_time_unit
        if math.isclose(self.remaining_time, 0):
            self.state = State.FINISHED

    def __str__(self):
        return f'{strings.PROCESS}{self.id}: {self.__class__.__name__}'

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, state={self.state}, '
                f'remaining_time={self.remaining_time})')


class Producer(Process):
    def __init__(self, append_item, **kwargs):
        super().__init__(**kwargs)
        self.append_item = append_item

    def run(self):
        super().run()
        if self.state == State.FINISHED:
            self.append_item(Item())


class Consumer(Process):
    def __init__(self, get_item, **kwargs):
        super().__init__(**kwargs)
        self.get_item = get_item
        self.item = None

    def run(self):
        try:
            self.item = self.item or self.get_item()
        except IndexError as e:
            raise EmptyInventoryError(e)
        super().run()
