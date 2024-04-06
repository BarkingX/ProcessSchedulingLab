import sys

from PySide6.QtWidgets import QApplication

from simulation.controller import SimulationController
from simulation.model.model import SimulationModel
from simulation.view import SimulationView

# # 创建主窗口

app = QApplication([])

model = SimulationModel()
view = SimulationView()
controller = SimulationController(model, view)

view.show()
sys.exit(app.exec())
