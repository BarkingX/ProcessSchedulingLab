import re

from PySide6.QtCore import QTimer

from simulation.strings import Strings
from simulation.model.model import *
from simulation.model.scheduler import RoundRobinScheduler
from simulation.util import is_valid_floatnumber, Timer
from simulation.view import SchedulingView


class SchedulingController:
    def __init__(self, scheduling_model: SchedulingModel,
                 view: SchedulingView, tablemodel: ProcessTableModel,
                 runnable_queue_model: ProcessQueueModel,
                 blocked_queue_model: ProcessQueueModel):
        self.scheduling_model = scheduling_model
        self.view = view
        self._tablemodel = tablemodel
        self._runnable_queue_model = runnable_queue_model
        self._blocked_queue_model = blocked_queue_model

        self.timer = Timer(1)
        self.scheduler = RoundRobinScheduler(self.timer, self.scheduling_model)
        self.qtimer = QTimer(self.view)

    def configure_view(self):
        self.view.set_create_process(self._create_process)
        self.view.set_next_turn(self._next_turn)
        self.view.set_process_table_model(self._tablemodel)
        self.view.set_runnable_model(self._runnable_queue_model)
        self.view.set_blocked_model(self._blocked_queue_model)
        self.view.set_pause_resume(self._pause_resume)
        self.view.set_reset_simulation(self._reset_simulation)

    def _create_process(self):
        process_type, burst_time = self.view.process_type_and_burst_time()
        if is_valid_floatnumber(burst_time):
            self._tablemodel.begin_append_row()
            self._runnable_queue_model.begin_append_row()
            self.scheduling_model.add_process_by_type(process_type,
                                                      burst_time=float(burst_time))
            self._tablemodel.end_append_row()
            self._runnable_queue_model.end_append_row()

    def _next_turn(self):
        if self.scheduler.running:
            self.update_ui_on_process(self.scheduler.running)

        if (len(self.scheduling_model.runnables) > 0
                or len(self.scheduling_model.blockeds) > 0
                or self.scheduler.running):
            self.scheduler.scheduling()

        if self.scheduler.running:
            self.update_ui_on_process(self.scheduler.running)

    def update_ui_on_process(self, p):
        self._tablemodel.update_row(self.scheduling_model.processes.index(p))
        self._runnable_queue_model.update_row(0)
        self._blocked_queue_model.update_row(0)
        self.view.update_labels(self.timer.now(), p.id,
                                self.scheduling_model.item_count())
        self.view.process_table_view.viewport().update()
        self.view.runnable_queue_view.viewport().update()
        self.view.blocked_queue_view.viewport().update()

    def _pause_resume(self):
        def _start_simulation():
            self.qtimer.timeout.connect(self._next_turn)
            self.qtimer.start(1000)
            self.view.pause_resume_action.setText(Strings.PAUSE_RESUME.split('/')[0])

        def _pause_simulation():
            self.qtimer.stop()
            self.view.pause_resume_action.setText(Strings.PAUSE_RESUME.split('/')[1])

        if self.qtimer.isActive():
            _pause_simulation()
        else:
            _start_simulation()

    def _reset_simulation(self):
        pass
