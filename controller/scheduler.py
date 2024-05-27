from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, model, timer, logger, quantum=3):
        self._model = model
        self._timer = timer
        self._logger = logger
        self._quantum = quantum
        self._status = SchedulerStatus()

    def reset(self):
        self._status.reset()
        self._timer.reset()

    @property
    def running(self):
        return (self._status.last_running if self._status.no_running_process()
                else self._status.running)

    @property
    def last_running(self):
        return self._status.last_running

    def scheduling(self):
        if self._status.no_running_process():
            self._timer.reset_elapsed()
            self._try_unblock_if_possible()
            if not self._model.has_runnable():
                raise NoRunnableProcessesError()
            self._status.set_running(self._model.dequeue_runnables())
            self.log_and_transition(self._status.running, Transition.READY_RUNNING)

        self._run_process(self._status.running)
        self._handle_process_completion_or_quantum_expiry(self._status.running)
        self._status.update()

    def _try_unblock_if_possible(self):
        if self._model.has_blocked() and self._model.item_count > 0:
            process = self._model.dequeue_blockeds()
            self.log_and_transition(process, Transition.BLOCKED_READY)
            self._model.enqueue_runnable(process)

    def log_and_transition(self, p, t):
        self._logger.log(self._timer.now, p, t)
        p.state = t.after()

    def _run_process(self, process):
        try:
            if self._timer.within(self._quantum):
                process.run()
                self._timer.increment()
        except EmptyInventoryError:
            self.log_and_transition(process, Transition.RUNNING_BLOCKED)
            self._model.enqueue_blocked(process)

    def _handle_process_completion_or_quantum_expiry(self, process):
        if process.remaining_time <= 0:
            self.log_and_transition(process, Transition.RUNNING_FINISHED)
        elif not self._timer.within(self._quantum):
            self.log_and_transition(process, Transition.RUNNING_READY)
            self._model.enqueue_runnable(process)


class SchedulerStatus:
    def __init__(self):
        self.running = None
        self.last_running = None

    def set_running(self, process):
        self.running = process

    def no_running_process(self):
        return self.running is None

    def reset(self):
        self.reset_running()
        self.last_running = None

    def update(self):
        if self.running.state != State.RUNNING:
            self.reset_running()

    def reset_running(self):
        self.last_running = self.running
        self.running = None
