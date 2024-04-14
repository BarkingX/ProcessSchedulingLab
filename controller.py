import re

from PySide6.QtCore import QTimer

from simulation.strings import Strings
from simulation.model.model import *
from simulation.model.scheduler import RoundRobinScheduler
from simulation.util import is_valid_floatnumber, NoRunnableProcessesError, Log
from simulation.view import SchedulingView


class SchedulingController:
    def __init__(self, scheduling_model: SchedulingModel,
                 view: SchedulingView, tablemodel: ProcessTableModel,
                 runnable_queue_model: ProcessQueueModel,
                 blocked_queue_model: ProcessQueueModel):
        self._scheduling_model = scheduling_model
        self._view = view
        self._tablemodel = tablemodel
        self._runnable_listmodel = runnable_queue_model
        self._blocked_listmodel = blocked_queue_model

        self._scheduler = RoundRobinScheduler(self._scheduling_model)
        self._qtimer = QTimer(self._view)
        self._qtimer.timeout.connect(self._next_turn)

        self._log_tablemodel = LogTableModel(self._view, Log.metadata,
                                             self._scheduler.logs())

    def configure_view(self):
        self._view.set_process_tablemodel(self._tablemodel)
        self._view.set_runnable_listmodel(self._runnable_listmodel)
        self._view.set_blocked_listmodel(self._blocked_listmodel)
        self._view.set_pause_resume(self._pause_resume)
        self._view.set_next_turn(self._next_turn)
        self._view.set_reset_simulation(self.reset_simulation)
        self._view.set_create_process(self._create_process)
        self._view.set_show_log(self._show_log)

    def _show_log(self):
        self._view.set_log_tablemodel(None)
        self._view.set_log_tablemodel(self._log_tablemodel)
        self._view.log_table_dialog.exec()

    def _pause_resume(self):
        self.pause_simulation() if self._qtimer.isActive() else self.start_simulation()

    def pause_simulation(self):
        self._qtimer.stop()
        self._view.pause_resume_action.setText(Strings.RESUME)

    def start_simulation(self):
        self._qtimer.start(1000)
        self._view.pause_resume_action.setText(Strings.PAUSE)

    def _next_turn(self):
        if self._scheduler.running:
            self.update_ui_on_process(self._scheduler.running)
        try:
            self._scheduler.scheduling()
        except NoRunnableProcessesError:
            self.pause_simulation()
        if self._scheduler.running:
            self.update_ui_on_process(self._scheduler.running)

    def reset_simulation(self):
        self._scheduler.reset()
        self._scheduling_model.clear_all()
        self._view.update_labels(0, None, 0)
        self._view.update_views()

    def update_ui_on_process(self, p):
        try:
            self._tablemodel.update_row(self._scheduling_model.processes.index(p))
        except ValueError:
            self._tablemodel.update_row(0)
        self._runnable_listmodel.update_row(0)
        self._blocked_listmodel.update_row(0)
        self._view.update_labels(self._scheduler.now(), p.id,
                                 self._scheduling_model.item_count())
        self._view.update_views()

    def _create_process(self):
        process_type, burst_time = self._view.process_type_and_burst_time()
        if is_valid_floatnumber(burst_time):
            self._tablemodel.begin_append_row()
            self._runnable_listmodel.begin_append_row()
            self._scheduling_model.add_process_by_type(process_type,
                                                       burst_time=float(burst_time))
            self._tablemodel.end_append_row()
            self._runnable_listmodel.end_append_row()
