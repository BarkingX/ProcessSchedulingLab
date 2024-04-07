import re

from simulation.model.model import SimulationModel
from simulation.view import SimulationView


class SimulationController:
    def __init__(self, model: SimulationModel, view: SimulationView):
        self.model = model
        self.view = view

    def configure_view(self):
        (self.view.set_create_process(self._create_process)
         .set_next_turn(self._next_turn)
         .set_reset_simulation(self._reset_simulation))

    def _create_process(self):
        process_type, burst_time = self.view.process_type_and_burst_time()
        if re.fullmatch(r'(\d*[.])?\d+', burst_time):
            p = self.model.new_type(process_type, burst_time=float(burst_time))
            self.model.add_process(p)
            self.view.append_process_table(p.to_record())
        self._update_queue_views(self.model.runnable, self.model.blocked)

    def _update_queue_views(self, runnable, blocked):
        self.view.update_runnable_queue(str(r) for r in runnable)
        self.view.update_blocked_queue(str(b) for b in blocked)

    def _next_turn(self):
        self.model.timer.next()
        self.view.update_process_table(p.to_record() for p in self.model.processes)
        self._update_queue_views(self.model.runnable, self.model.blocked)

    def start_simulation(self):
        pass
        # self.service.start_simulation(self.model)
        # 在这里可以添加更新视图的逻辑

    def pause_simulation(self):
        pass
        # self.service.pause_simulation(self.model)
        # 在这里可以添加更新视图的逻辑

    def _reset_simulation(self):
        self._update_queue_views([], [])
