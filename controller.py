import re

from PySide6.QtCore import QTimer

from simulation.model.model import *
from simulation.model.scheduler import RoundRobinScheduler
from simulation.util import is_valid_floatnumber, Timer, State
from simulation.view import SchedulingView


class SchedulingController:
    def __init__(self, scheduling_model: SchedulingModel,
                 view: SchedulingView, tablemodel: ProcessTableModel,
                 runnable_queue_model: ProcessQueueModel,
                 blocked_queue_model: ProcessQueueModel):
        self.scheduling_model = scheduling_model
        self.view = view
        self.tablemodel = tablemodel
        self.runnable_queue_model = runnable_queue_model
        self.blocked_queue_model = blocked_queue_model

        self.timer = Timer(1)
        self.scheduler = RoundRobinScheduler(self.timer, self.scheduling_model)

        self.qtimer = QTimer(self.view)
        self.qtimer.timeout.connect(self._next_turn)
        self.qtimer.start(1000)

    def configure_view(self):
        self.view.set_create_process(self._create_process)
        self.view.set_next_turn(self._next_turn)
        self.view.set_process_table_model(self.tablemodel)
        self.view.set_runnable_model(self.runnable_queue_model)
        self.view.set_blocked_model(self.blocked_queue_model)
        self.view.set_reset_simulation(self._reset_simulation)

    def _create_process(self):
        process_type, burst_time = self.view.process_type_and_burst_time()
        if is_valid_floatnumber(burst_time):
            self.tablemodel.begin_append_row()
            self.runnable_queue_model.begin_append_row()
            self.scheduling_model.add_type(process_type, burst_time=float(burst_time))
            self.tablemodel.end_append_row()
            self.runnable_queue_model.end_append_row()

    def _next_turn(self):
        self.scheduler.scheduling()
        self.update_ui(self.scheduler.running)

    def update_ui(self, p):
        self.tablemodel.update_row(self.scheduling_model.processes.index(p))
        self.runnable_queue_model.update_row(0)
        self.blocked_queue_model.update_row(0)
        self.view.update_labels(self.timer.now(), p.id,
                                len(self.scheduling_model.inventory))

    def start_simulation(self):
        pass
        # 在这里可以添加更新视图的逻辑

    def pause_simulation(self):
        pass
        # 在这里可以添加更新视图的逻辑

    def _reset_simulation(self):
        pass
