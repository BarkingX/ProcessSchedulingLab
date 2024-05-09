import sys
from PySide6.QtWidgets import QApplication
from simulation.strings import Strings
from simulation.model import (SchedulingModel, ProcessTableModel, ProcessQueueModel,
                              Process)
from simulation.controller import SchedulingController
from simulation.view import SchedulingView


def main():
    app = QApplication(sys.argv)
    scheduling_model = SchedulingModel()
    view = SchedulingView()
    tablemodel = ProcessTableModel(view, Process.metadata, scheduling_model.processes)
    runnable_listmodel = ProcessQueueModel(view, [Strings.PROCESS],
                                           scheduling_model.runnables)
    blocked_listmodel = ProcessQueueModel(view, [Strings.PROCESS],
                                          scheduling_model.blockeds)
    controller = SchedulingController(scheduling_model, view, tablemodel,
                                      runnable_listmodel, blocked_listmodel)
    try:
        controller.setup_view()
        view.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
