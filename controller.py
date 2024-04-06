import re

from simulation.model.model import SimulationModel
from simulation.view import SimulationView


class SimulationController:
    def __init__(self, model: SimulationModel, view: SimulationView):
        self.model = model
        self.view = view
        (self.view.set_create_process(self._create_process)
                  .set_next_turn(self._next_turn))

    def _create_process(self):
        process_type, burst_time = self.view.process_type_and_burst_time()
        if re.fullmatch(r'(\d*[.])?\d+', burst_time):
            p = self.model.new_type(process_type, burst_time=float(burst_time))
            self.model.add_process(p)
            self.view.append_process_table(p.to_record())

    def _next_turn(self):
        self.model.processes[0].remaining_time -= 1
        self.model.timer.next()
        self.view.update_process_table(p.to_record() for p in self.model.processes)

    def start_simulation(self):
        pass
        # self.service.start_simulation(self.model)
        # 在这里可以添加更新视图的逻辑

    def pause_simulation(self):
        pass
        # self.service.pause_simulation(self.model)
        # 在这里可以添加更新视图的逻辑

    def reset_simulation(self):
        pass
        # self.service.reset_simulation(self.model)
        # 在这里可以添加更新视图的逻辑
