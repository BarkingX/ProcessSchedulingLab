import sys

from PySide6.QtWidgets import QApplication

from simulation.controller import SimulationController
from simulation.model.model import SimulationModel, ProcessTableModel, ProcessQueueModel
from simulation.view import SimulationView

# # 创建主窗口

app = QApplication(sys.argv)
model = SimulationModel()
view = SimulationView()
tablemodel = ProcessTableModel(view, ['id', 'type', 'state', 'remaining_time'],
                               model.processes)
runnable_queue_model = ProcessQueueModel(view, model.runnable)
blocked_queue_model = ProcessQueueModel(view, model.blocked)

controller = SimulationController(model, view, tablemodel,
                                  runnable_queue_model, blocked_queue_model)

controller.configure_view()

view.show()
sys.exit(app.exec())
