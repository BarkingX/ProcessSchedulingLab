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
    def running(self):
        return (self._status.last_running if self._status.no_running_process()
                else self._status.running)

    @property
    def now(self):
        return self._timer.now

    @property
    def logs(self):
        return self._logger.logs

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
            self.execute_command(PickUpCommand(self), self._model.dequeue_runnables())

        self._run_process(self._status.running)
        self._update_process_state(self._status.running)
        self._status.update()

    def _try_unblock_if_possible(self):
        if self._model.has_blocked() and self._model.item_count > 0:
            self.execute_command(AwakeCommand(self), self._model.dequeue_blockeds())

    def _run_process(self, process):
        try:
            if self._timer.within(self._quantum):
                process.run()
                self._timer.increment()
        except EmptyInventoryError:
            self.execute_command(BlockCommand(self), process)

    def _update_process_state(self, process):
        if process.remaining_time <= 0:
            self.execute_command(CompleteCommand(self), process)
        elif not self._timer.within(self._quantum):
            self.execute_command(ExpiryCommand(self), process)

    def execute_command(self, command, process):
        self._logger.log(self._timer.now, process, command.execute(process))

    def set_running(self, process):
        self._status.running = process

    def enqueue_runnable(self, process):
        self._model.enqueue_runnable(process)

    def enqueue_blocked(self, process):
        self._model.enqueue_blocked(process)
