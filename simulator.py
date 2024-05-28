import sys

from PySide6.QtWidgets import QApplication
from simulation.model import (SchedulingModel)
from simulation.controller import SchedulingController
from simulation.view import SchedulingView


class Simulator:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self.model = SchedulingModel()
        self.view = SchedulingView()
        self.controller = SchedulingController(self.model, self.view)

    def start(self):
        try:
            self.controller.setup_view()
            self.view.show()
            sys.exit(self._app.exec_())
        except Exception as e:
            print(e, file=sys.stderr)
