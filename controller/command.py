from abc import ABC

from simulation.util import Transition


class TransitionCommand(ABC):
    transition = None

    def __init__(self, scheduler):
        self._scheduler = scheduler

    def execute(self, process):
        process.set_state(self.transition.after())
        self._execute(process)
        return self.transition

    def _execute(self, process):
        pass


class AwakeCommand(TransitionCommand):
    transition = Transition.BLOCKED_READY

    def _execute(self, process):
        self._scheduler.enqueue_runnable(process)


class PickUpCommand(TransitionCommand):
    transition = Transition.READY_RUNNING

    def _execute(self, process):
        self._scheduler.set_running(process)


class BlockCommand(TransitionCommand):
    transition = Transition.RUNNING_BLOCKED

    def _execute(self, process):
        self._scheduler.enqueue_blocked(process)


class CompleteCommand(TransitionCommand):
    transition = Transition.RUNNING_FINISHED


class ExpiryCommand(TransitionCommand):
    transition = Transition.RUNNING_READY

    def _execute(self, process):
        self._scheduler.enqueue_runnable(process)


class InitializeCommand(TransitionCommand):
    transition = Transition.INITIALIZED_READY
