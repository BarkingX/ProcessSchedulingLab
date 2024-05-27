from simulation.util import *


class RoundRobinScheduler:
    def __init__(self, model, timer, logger, quantum=3):
        self.model = model
        self.timer = timer
        self.logger = logger
        self.quantum = quantum
        self.running = None
        self.last_running = None

    def reset(self):
        self.running = None
        self.last_running = None
        self.timer.reset()

    def scheduling(self):
        if not self.running:
            self.timer.reset_elapsed()
            self._try_unblock_if_possible()
            if len(self.model.runnables) == 0:
                raise NoRunnableProcessesError()
            self.running = self.model.dequeue_runnables()
            self.log_and_transition(self.running, Transition.READY_RUNNING)

        self._run_process(self.running)

        if not self.running.state == State.RUNNING:
            self.last_running = self.running
            self.running = None

    def _try_unblock_if_possible(self):
        if len(self.model.blockeds) > 0 and len(self.model.inventory) > 0:
            process = self.model.dequeue_blockeds()
            self.log_and_transition(process, Transition.BLOCKED_READY)
            self.model.enqueue_runnable(process)

    def log_and_transition(self, p, t):
        self.logger.log(self.timer.now, p, t)
        p.state = t.after()

    def _run_process(self, process):
        try:
            if self.timer.within(self.quantum):
                process.run()
                self.timer.increment()
        except EmptyInventoryError:
            self.log_and_transition(process, Transition.RUNNING_BLOCKED)
            self.model.enqueue_blocked(process)

        self._handle_process_completion_or_quantum_expiry(process)

    def _handle_process_completion_or_quantum_expiry(self, process):
        if process.remaining_time <= 0:
            self.log_and_transition(process, Transition.RUNNING_FINISHED)
        elif not self.timer.within(self.quantum):
            self.log_and_transition(process, Transition.RUNNING_READY)
            self.model.enqueue_runnable(process)
