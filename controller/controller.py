from PySide6.QtCore import QTimer

from simulation.strings import Strings
from simulation.model import (SchedulingModel, ProcessTableModel, ProcessQueueModel,
                              LogTableModel, Process)
from simulation.controller.scheduler import RoundRobinScheduler
from simulation.util import (NoRunnableProcessesError, Log)
from simulation.view import SchedulingView


class SchedulingController:
    TIMER_INTERVAL_MS = 1000

    def __init__(self, model: SchedulingModel,
                 view: SchedulingView):
        self._model = model
        self._view = view

        self._qtimer = QTimer(self._view)
        self._qtimer.timeout.connect(self._handle_timer_timeout)

        self._scheduler = RoundRobinScheduler(self._model)
        self._log_tablemodel = LogTableModel(self._view, Log.metadata,
                                             self._scheduler.logs)
        self._tablemodel = ProcessTableModel(self._view, Process.metadata,
                                             self._model.processes)
        self._runnable_listmodel = ProcessQueueModel(self._view, [Strings.PROCESS],
                                                     self._model.runnables)
        self._blocked_listmodel = ProcessQueueModel(self._view, [Strings.PROCESS],
                                                    self._model.blockeds)

    def setup_view(self):
        self._view.setup()
        self._view.set_process_tablemodel(self._tablemodel)
        self._view.set_runnable_listmodel(self._runnable_listmodel)
        self._view.set_blocked_listmodel(self._blocked_listmodel)
        self._view.set_next_turn_callback(self._handle_timer_timeout)
        self._view.set_pause_resume_callback(self.pause_resume)
        self._view.set_reset_simulation_callback(self.reset_simulation)
        self._view.set_create_process_callback(self._create_process)
        self._view.set_show_log_callback(self._show_log)

    def _handle_timer_timeout(self):
        try:
            self._scheduler.scheduling()
        except NoRunnableProcessesError:
            self.pause_resume()
        self._update_ui_on_process(self._scheduler.running)

    def pause_resume(self):
        self.pause_simulation() if self._qtimer.isActive() else self.start_simulation()

    def pause_simulation(self):
        self._qtimer.stop()
        self._view.stop_progress()
        self._set_control_text(Strings.RESUME)

    def start_simulation(self):
        self._qtimer.start(self.TIMER_INTERVAL_MS)
        self._view.start_progress()
        self._set_control_text(Strings.PAUSE)

    def _set_control_text(self, control_text):
        self._view.pause_resume_action.setText(control_text)

    def _update_ui_on_process(self, p):
        self._tablemodel.update_row(self._model.process_index(p))
        self._runnable_listmodel.update_row(0)
        self._blocked_listmodel.update_row(0)
        self._view.update_labels(self._scheduler.now, p.id,
                                 self._model.item_count)
        self._view.update_views()

    def reset_simulation(self):
        self.reset()
        self.update_view(0, None, 0)

    def reset(self):
        self._scheduler.reset()
        self._model.reset()

    def update_view(self, *labels):
        self._view.update_labels(*labels)
        self._view.update_views()

    def _create_process(self):
        self._tablemodel.begin_append_row()
        self._runnable_listmodel.begin_append_row()
        self._model.add_new_process(*self._view.process_params())
        self._scheduler.welcome_new_process()
        self._tablemodel.end_append_row()
        self._runnable_listmodel.end_append_row()

    def _show_log(self):
        self._view.set_log_tablemodel(None)
        self._view.set_log_tablemodel(self._log_tablemodel)
        self._view.log_table_dialog.exec()
