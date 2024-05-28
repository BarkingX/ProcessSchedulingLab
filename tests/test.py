import unittest
from simulation.model import SchedulingModel
from simulation.controller.scheduler import RoundRobinScheduler, NoRunnableProcessesError
from simulation.controller.util import RoundRobinTimer, RoundRobinLogger
from simulation.strings import Strings
from simulation.util import State


class RoundRobinSchedulerTest(unittest.TestCase):
    def setUp(self):
        self.scheduling_model = SchedulingModel()
        self.scheduler = RoundRobinScheduler(self.scheduling_model,
                                             RoundRobinTimer(), RoundRobinLogger())

    def add_producers(self, count):
        for _ in range(count):
            self.scheduling_model.add_new_process(Strings.PRODUCER_EN, 5)

    def add_consumers(self, count):
        for _ in range(count):
            self.scheduling_model.add_new_process(Strings.CONSUMER_EN, 5)

    def run_scheduler(self):
        try:
            while True:
                self.scheduler.scheduling()
        except NoRunnableProcessesError:
            pass

    def test_multiple_producers_and_consumers(self):
        self.add_producers(5)
        self.add_consumers(4)
        self.run_scheduler()

        for log in self.scheduler.logs:
            print(log)

        self.assertEqual(len(self.scheduling_model.inventory), 1)
        self.assertTrue(self.scheduler.running.state == State.FINISHED)
        self.assertFalse(self.scheduling_model.has_runnable())
        self.assertFalse(self.scheduling_model.has_blocked())


if __name__ == '__main__':
    unittest.main()
