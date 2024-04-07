import sys

from PySide6.QtWidgets import QApplication

from simulation.controller import SimulationController
from simulation.model.model import SimulationModel
from simulation.view import SimulationView

# # 创建主窗口

app = QApplication(sys.argv)
model = SimulationModel()
view = SimulationView()
controller = SimulationController(model, view)
controller.configure_view()

view.show()
sys.exit(app.exec())
