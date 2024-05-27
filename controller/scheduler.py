from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, model, timer, logger, quantum=3):
        self._model = model
        self._timer = timer
        self._logger = logger
        self._quantum = quantum
        self._status = SchedulerStatus()

    @property
    def running(self):
        return (self._status.last_running if self._status.no_running_process()
                else self._status.running)

    def reset(self):
        self._status.reset()
        self._timer.reset()

    def scheduling(self):
        if self._status.no_running_process():
            self._timer.reset_elapsed()
            self._try_unblock_if_possible()
            if not self._model.has_runnable():
                raise NoRunnableProcessesError()
            self._status.running = self._model.dequeue_runnables()
            self._handle_pickup(self._status.running)

        self._run_process(self._status.running)
        self._update_process_state(self._status.running)
        self._status.update()

    def _try_unblock_if_possible(self):
        if self._model.has_blocked() and self._model.item_count > 0:
            self._handle_awake_blocked(self._model.dequeue_blockeds())

    def _handle_awake_blocked(self, blocked):
        self.log_and_transition(blocked, Transition.BLOCKED_READY)
        self._model.enqueue_runnable(blocked)

    def log_and_transition(self, p, t):
        self._logger.log(self._timer.now, p, t)
        p.state = t.after()

    def _handle_pickup(self, ready):
        self.log_and_transition(ready, Transition.READY_RUNNING)

    def _run_process(self, process):
        try:
            if self._timer.within(self._quantum):
                process.run()
                self._timer.increment()
        except EmptyInventoryError:
            self._handle_inventory_empty(process)

    def _handle_inventory_empty(self, process):
        self.log_and_transition(process, Transition.RUNNING_BLOCKED)
        self._model.enqueue_blocked(process)

    def _update_process_state(self, process):
        if process.remaining_time <= 0:
            self._handle_process_completion(process)
        elif not self._timer.within(self._quantum):
            self._handle_quantum_expiry(process)

    def _handle_process_completion(self, process):
        self.log_and_transition(process, Transition.RUNNING_FINISHED)

    def _handle_quantum_expiry(self, process):
        self.log_and_transition(process, Transition.RUNNING_READY)
        self._model.enqueue_runnable(process)

    def handle_process_initialized(self, process):
        self.log_and_transition(process, Transition.INITIALIZED_READY)


class SchedulerStatus:
    def __init__(self):
        self.running = None
        self.last_running = None

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
