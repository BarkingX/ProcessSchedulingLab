import itertools
import math
import re

from simulation.strings import Strings
from simulation.util import State, EmptyInventoryError, Item

producer_pattern = re.compile('producer', re.I)


class Process:
    metadata = (Strings.PROCESS_ID, Strings.PROCESS_STATE,
                Strings.PROCESS_TYPE, Strings.PROCESS_REMAINING_TIME)
    _id_generator = itertools.count(0)
    _working_time_unit = 1
    _default_burst_time = 5 * _working_time_unit

    def __init__(self, burst_time=_default_burst_time):
        self.id = next(self._id_generator)
        self.state = State.READY
        self._remaining_time = burst_time
        self.elapsed_time = burst_time

    @property
    def remaining_time(self):
        return self._remaining_time

    @remaining_time.setter
    def remaining_time(self, value):
        self._remaining_time = value if value > 0 else 0

    def run(self):
        self.remaining_time -= self._working_time_unit

    def __str__(self):
        return f'{Strings.PROCESS}{self.id}: {self.__class__.__name__}'

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, state={self.state}, '
                f'remaining_time={self.remaining_time})')

class Producer(Process):
    def __init__(self, append_item, **kwargs):
        super().__init__(**kwargs)
        self.append_item = append_item

    def run(self):
        super().run()
        if math.isclose(0, self.remaining_time):
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
