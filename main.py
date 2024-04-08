import sys

from PySide6.QtWidgets import QApplication

from simulation.controller import SchedulingController
from simulation.model.model import SchedulingModel, ProcessTableModel, ProcessQueueModel
from simulation.view import SchedulingView

# # 创建主窗口

app = QApplication(sys.argv)
scheduling_model = SchedulingModel()
view = SchedulingView()
tablemodel = ProcessTableModel(view, ['id', 'type', 'state', 'remaining_time'],
                               scheduling_model.processes)
runnable_queue_model = ProcessQueueModel(view, scheduling_model.runnable)
blocked_queue_model = ProcessQueueModel(view, scheduling_model.blocked)

controller = SchedulingController(scheduling_model, view, tablemodel,
                                  runnable_queue_model, blocked_queue_model)

controller.configure_view()

view.show()
sys.exit(app.exec())
