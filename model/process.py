import itertools
import math

from simulation.strings import Strings
from simulation.util import State, EmptyInventoryError, Item


class Process:
    metadata = (Strings.PROCESS_ID, Strings.PROCESS_TYPE,
                Strings.PROCESS_STATE, Strings.PROCESS_REMAINING_TIME)
    _id_generator = itertools.count(0)
    _working_time_unit = 1
    _default_burst_time = 5 * _working_time_unit

    def __init__(self, burst_time=None):
        if burst_time is None:
            burst_time = self._default_burst_time
        self.id = next(self._id_generator)
        self.state = State.READY
        self._remaining_time = burst_time

    @property
    def remaining_time(self):
        return self._remaining_time

    @remaining_time.setter
    def remaining_time(self, value):
        self._remaining_time = max(0, value)

    def set_state(self, state):
        self.state = state

    def run(self):
        if self.remaining_time > 0:
            self.remaining_time -= self._working_time_unit

    def __str__(self):
        return f'{Strings.PROCESS}{self.id}: {self.__class__.__name__}'

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, state={self.state}, '
                f'remaining_time={self.remaining_time})')


class Producer(Process):
    def __init__(self, append_item, burst_time=None):
        super().__init__(burst_time)
        self.append_item = append_item

    def run(self):
        super().run()
        if math.isclose(0, self.remaining_time):
            self.append_item(Item())


class Consumer(Process):
    def __init__(self, get_item, burst_time=None):
        super().__init__(burst_time)
        self.get_item = get_item
        self.item = None

    def run(self):
        try:
            self.item = self.item or self.get_item()
        except IndexError as e:
            raise EmptyInventoryError(e)
        super().run()


class ProcessCreator:
    def __init__(self, buffer):
        self._buffer = buffer

    def create_process(self, ptype, burst_time):
        return {
            Strings.PRODUCER_EN: self.create_producer,
            Strings.CONSUMER_EN: self.create_consumer,
        }.get(str.lower(ptype), self.create_producer)(burst_time)

    def create_producer(self, burst_time):
        return Producer(self._buffer.append, float(burst_time))

    def create_consumer(self, burst_time):
        return Consumer(self._buffer.pop, float(burst_time))
