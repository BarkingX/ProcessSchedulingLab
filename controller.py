import re

from simulation.model.model import *
from simulation.util import is_valid_floatnumber
from simulation.view import SimulationView


class SimulationController:
    def __init__(self, model: SimulationModel,
                 view: SimulationView, tablemodel: ProcessTableModel,
                 runnable_queue_model: ProcessQueueModel,
                 blocked_queue_model: ProcessQueueModel):
        self.model = model
        self.view = view
        self.tablemodel = tablemodel
        self.runnable_queue_model = runnable_queue_model
        self.blocked_queue_model = blocked_queue_model

    def configure_view(self):
        (self.view.set_create_process(self._create_process)
         .set_next_turn(self._next_turn)
         .set_process_table_model(self.tablemodel)
         .set_runnable_model(self.runnable_queue_model)
         .set_blocked_model(self.blocked_queue_model)
         .set_reset_simulation(self._reset_simulation))

    def _create_process(self):
        process_type, burst_time = self.view.process_type_and_burst_time()
        if is_valid_floatnumber(burst_time):
            p = self.model.new_type(process_type, burst_time=float(burst_time))
            self.tablemodel.begin_append_row()
            self.runnable_queue_model.begin_append_row()
            self.model.add_process(p)
            self.tablemodel.end_append_row()
            self.runnable_queue_model.end_append_row()

    def _next_turn(self):
        self.model.timer.next()

    def start_simulation(self):
        pass
        # 在这里可以添加更新视图的逻辑

    def pause_simulation(self):
        pass
        # 在这里可以添加更新视图的逻辑

    def _reset_simulation(self):
        pass
