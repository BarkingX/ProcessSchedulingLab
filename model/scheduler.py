from simulation.util import *


def _log_transition(logs, time, trans, procs):
    logs.append(Log(time, trans, procs))


class RoundRobinScheduler:
    def __init__(self, model, quantum=3):
        self.model = model
        self.quantum = quantum
        self.running = None
        self.last_running = None
        self.time_now = 0
        self._time_elapsed = 0
        self.logs = []

    def reset(self):
        self.running = None
        self.last_running = None
        self.time_now = 0
        self._time_elapsed = 0
        self.logs.clear()

    def scheduling(self):
        if not self.running:
            self._time_elapsed = 0
            self._try_unblock_if_possible()
            if len(self.model.runnables) == 0:
                raise NoRunnableProcessesError()
            self.running = self.model.runnables.popleft()
            self._log_and_transition(Transition.READY_RUNNING, self.running)

        self._run_process(self.running)

        if not self.running.state == State.RUNNING:
            self.last_running = self.running
            self.running = None

    def _try_unblock_if_possible(self):
        if len(self.model.blockeds) > 0 and len(self.model.inventory) > 0:
            self._log_and_transition(Transition.BLOCKED_READY,
                                     self.model.blockeds.popleft(),
                                     post_trans_callback=self.model.runnables.appendleft)

    def _log_and_transition(self, t, p, *, post_trans_callback=no_operation):
        _log_transition(self.logs, self.time_now, t, p)
        p.state = t.after()
        post_trans_callback(p)

    def _run_process(self, process):
        try:
            self._execute_process(process)
        except EmptyInventoryError:
            self._log_and_transition(Transition.RUNNING_BLOCKED, process,
                                     post_trans_callback=self.model.blockeds.append)
        self._handle_process_completion_or_quantum_expiry(process)

    def _execute_process(self, process):
        if self._time_elapsed < self.quantum:
            process.run()
            self.time_now += 1
            self._time_elapsed += 1

    def _handle_process_completion_or_quantum_expiry(self, process):
        if process.remaining_time <= 0:
            self._log_and_transition(Transition.RUNNING_FINISHED, process)
        elif self._time_elapsed >= self.quantum:
            self._log_and_transition(Transition.RUNNING_READY, process,
                                     post_trans_callback=self.model.runnables.append)
