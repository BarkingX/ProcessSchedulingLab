import sys

from PySide6.QtWidgets import QApplication

from simulation.model.process import Process
from simulation.strings import Strings
from simulation.controller import SchedulingController
from simulation.model.model import SchedulingModel, ProcessTableModel, ProcessQueueModel
from simulation.view import SchedulingView


app = QApplication(sys.argv)
scheduling_model = SchedulingModel()
view = SchedulingView()

tablemodel = ProcessTableModel(view, Process.metadata, scheduling_model.processes)
runnable_queue_model = ProcessQueueModel(view, [Strings.PROCESS],
                                         scheduling_model.runnables)
blocked_queue_model = ProcessQueueModel(view, [Strings.PROCESS],
                                        scheduling_model.blockeds)

controller = SchedulingController(scheduling_model,
                                  view, tablemodel,
                                  runnable_queue_model, blocked_queue_model)

controller.configure_view()

view.show()
sys.exit(app.exec())
