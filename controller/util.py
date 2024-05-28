from simulation.util import State, Log


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


class RoundRobinTimer:
    def __init__(self):
        self.time = 0
        self.elapsed = 0

    @property
    def now(self):
        return self.time

    def within(self, upper, lower=0):
        return lower <= self.elapsed < upper

    def reset(self):
        self.reset_time()
        self.reset_elapsed()

    def reset_time(self):
        self.time = 0

    def reset_elapsed(self):
        self.elapsed = 0

    def increment(self, by=1):
        self.increment_time(by=by)
        self.increment_elapsed(by=by)

    def increment_time(self, by=1):
        self.time += by

    def increment_elapsed(self, by=1):
        self.elapsed += by


class RoundRobinLogger:
    def __init__(self):
        self.logs = []

    def log(self, occur_time, process, transition):
        self.logs.append(Log(occur_time, process, transition))

    def reset(self):
        self.logs.clear()
