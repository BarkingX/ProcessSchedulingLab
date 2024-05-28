from simulation.controller.command import *
from simulation.controller.util import *
from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, model, quantum=3):
        self._model = model
        self._quantum = quantum
        self._timer = RoundRobinTimer()
        self._logger = RoundRobinLogger()
        self._status = SchedulerStatus()

    @property
    def last_process(self):
        return self._model.last_process

    @property
    def running(self):
        return (self._status.last_running if self._status.no_running_process()
                else self._status.running)

    @property
    def now(self):
        return self._timer.now

    @property
    def logs(self):
        return self._logger.logs

    def welcome_new_process(self):
        self._execute_command(InitializeCommand(self))

    def set_running(self, process):
        self._status.running = process

    def enqueue_runnable(self, process):
        self._model.enqueue_runnable(process)

    def enqueue_blocked(self, process):
        self._model.enqueue_blocked(process)

    def dequeue_runnable(self):
        return self._model.dequeue_runnable()

    def dequeue_blocked(self):
        return self._model.dequeue_blocked()

    def reset(self):
        self._logger.reset()
        self._status.reset()
        self._timer.reset()

    def scheduling(self):
        if self._status.no_running_process():
            self._timer.reset_elapsed()
            self._try_unblock_if_possible()
            if not self._model.has_runnable():
                raise NoRunnableProcessesError()
            self._execute_command(PickUpCommand(self))

        self._run_process()
        self._update_process_state()
        self._status.update()

    def _execute_command(self, command):
        self._logger.log(self._timer.now, *command.execute())

    def _try_unblock_if_possible(self):
        if self._model.has_blocked() and self._model.item_count > 0:
            self._execute_command(AwakeCommand(self))

    def _run_process(self):
        try:
            if self._timer.within(self._quantum):
                self.running.run()
                self._timer.increment()
        except EmptyInventoryError:
            self._execute_command(BlockCommand(self))

    def _update_process_state(self):
        if self.running.remaining_time <= 0:
            self._execute_command(CompleteCommand(self))
        elif not self._timer.within(self._quantum):
            self._execute_command(ExpiryCommand(self))
