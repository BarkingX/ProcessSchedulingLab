from abc import ABC

from simulation.util import Transition


class TransitionCommand(ABC):
    transition = None

    def __init__(self, scheduler):
        self._scheduler = scheduler
        self.process = None

    def execute(self):
        self.process.set_state(self.transition.after())
        self._execute()
        return self.process, self.transition

    def _execute(self):
        pass


class AwakeCommand(TransitionCommand):
    transition = Transition.BLOCKED_READY

    def __init__(self, scheduler):
        super().__init__(scheduler)
        self.process = self._scheduler.dequeue_blocked()

    def _execute(self):
        self._scheduler.enqueue_runnable(self.process)


class PickUpCommand(TransitionCommand):
    transition = Transition.READY_RUNNING

    def __init__(self, scheduler):
        super().__init__(scheduler)
        self.process = self._scheduler.dequeue_runnable()

    def _execute(self):
        self._scheduler.set_running(self.process)


class BlockCommand(TransitionCommand):
    transition = Transition.RUNNING_BLOCKED

    def __init__(self, scheduler):
        super().__init__(scheduler)
        self.process = self._scheduler.running

    def _execute(self):
        self._scheduler.enqueue_blocked(self.process)


class CompleteCommand(TransitionCommand):
    transition = Transition.RUNNING_FINISHED

    def __init__(self, scheduler):
        super().__init__(scheduler)
        self.process = self._scheduler.running


class ExpiryCommand(TransitionCommand):
    transition = Transition.RUNNING_READY

    def __init__(self, scheduler):
        super().__init__(scheduler)
        self.process = self._scheduler.running

    def _execute(self):
        self._scheduler.enqueue_runnable(self.process)


class InitializeCommand(TransitionCommand):
    transition = Transition.INITIALIZED_READY

    def __init__(self, scheduler):
        super().__init__(scheduler)
        self.process = self._scheduler.last_process
