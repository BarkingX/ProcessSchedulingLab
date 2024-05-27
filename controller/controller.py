from PySide6.QtCore import QTimer

from simulation.strings import Strings
from simulation.model import (SchedulingModel, ProcessTableModel, ProcessQueueModel,
                              LogTableModel)
from simulation.controller.scheduler import RoundRobinScheduler
from simulation.util import (NoRunnableProcessesError, Log, Transition,
                             RoundRobinLogger, RoundRobinTimer)
from simulation.view import SchedulingView


class SchedulingController:
    TIMER_INTERVAL_MS = 1000

    def __init__(self, scheduling_model: SchedulingModel,
                 view: SchedulingView, tablemodel: ProcessTableModel,
                 runnable_listmodel: ProcessQueueModel,
                 blocked_listmodel: ProcessQueueModel):
        self._scheduling_model = scheduling_model
        self._view = view
        self._tablemodel = tablemodel
        self._runnable_listmodel = runnable_listmodel
        self._blocked_listmodel = blocked_listmodel

        self._logger = RoundRobinLogger()
        self._scheduling_timer = RoundRobinTimer()
        self._scheduler = RoundRobinScheduler(self._scheduling_model,
                                              self._scheduling_timer, self._logger)
        self._log_tablemodel = LogTableModel(self._view, Log.metadata, self._logger.logs)
        self._qtimer = QTimer(self._view)
        self._qtimer.timeout.connect(self._handle_timer_timeout)

    def setup_view(self):
        self._view.setup()
        self._view.set_process_tablemodel(self._tablemodel)
        self._view.set_runnable_listmodel(self._runnable_listmodel)
        self._view.set_blocked_listmodel(self._blocked_listmodel)
        self._view.set_next_turn_callback(self._handle_timer_timeout)
        self._view.set_pause_resume_callback(self._pause_resume)
        self._view.set_reset_simulation_callback(self._reset_simulation)
        self._view.set_create_process_callback(self._create_process)
        self._view.set_show_log_callback(self._show_log)

    def _handle_timer_timeout(self):
        def _update_ui_on_process(p):
            self._tablemodel.update_row(self._scheduling_model.process_index(p))
            self._runnable_listmodel.update_row(0)
            self._blocked_listmodel.update_row(0)
            self._view.update_labels(self._scheduling_timer.now, p.id,
                                     self._scheduling_model.item_count)
            self._view.update_views()

        if self._scheduler.running:
            _update_ui_on_process(self._scheduler.running)
        try:
            self._scheduler.scheduling()
        except NoRunnableProcessesError:
            self._pause_resume()

        if self._scheduler.running or len(self._scheduling_model.blockeds) > 0:
            _update_ui_on_process(self._scheduler.running if self._scheduler.running
                                  else self._scheduler.last_running)

    def _pause_resume(self):
        self._pause_simulation() if self._qtimer.isActive() else self._start_simulation()

    def _pause_simulation(self):
        self._qtimer.stop()
        self._view.stop_progress()
        self._view.pause_resume_action.setText(Strings.RESUME)

    def _start_simulation(self):
        self._qtimer.start(self.TIMER_INTERVAL_MS)
        self._view.start_progress()
        self._view.pause_resume_action.setText(Strings.PAUSE)

    def _reset_simulation(self):
        self._logger.clear()
        self._scheduler.reset()
        self._scheduling_model.reset()
        self._view.update_labels(0, None, 0)
        self._view.update_views()

    def _create_process(self):
        self._tablemodel.begin_append_row()
        self._runnable_listmodel.begin_append_row()
        self._scheduling_model.add_new_process(*self._view.process_params())
        self._scheduler.log_and_transition(self._scheduling_model.last_process,
                                           Transition.INITIALIZED_READY)
        self._tablemodel.end_append_row()
        self._runnable_listmodel.end_append_row()

    def _show_log(self):
        self._view.set_log_tablemodel(None)
        self._view.set_log_tablemodel(self._log_tablemodel)
        self._view.log_table_dialog.exec()
