from collections import deque
from typing import List, Any, Deque, Callable, Dict

from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PySide6.QtGui import QColor

from simulation.model import Producer, Consumer, Process
from simulation.strings import Strings


class SchedulingModel:
    def __init__(self):
        self.inventory: List[Any] = []
        self.processes: List[Process] = []
        self.runnables: Deque[Process] = deque()
        self.blockeds: Deque[Process] = deque()
        self._constructors: Dict[str, Callable[[float], Process]] = {
            Strings.PRODUCER_EN: lambda burst: Producer(self.inventory.append, burst),
            Strings.CONSUMER_EN: lambda burst: Consumer(self.inventory.pop, burst),
        }

    def item_count(self):
        return len(self.inventory)

    def process_index(self, p):
        try:
            return self.processes.index(p)
        except ValueError:
            return 0

    def clear_all(self):
        for collection in [self.processes, self.runnables, self.inventory, self.blockeds]:
            collection.clear()

    def add_new_process_of(self, process_type, burst_time):
        p_constructor = self._constructors.get(process_type.lower())
        self.add_new_process(p_constructor(burst_time))

    def add_new_process(self, process):
        self.processes.append(process)
        self.runnables.append(process)


class TableModel(QAbstractTableModel):
    _column_map = {}
    _lightgray = QColor(230, 230, 230)

    def __init__(self, parent, header, data):
        super().__init__(parent)
        self._header = header
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        def on_display():
            renderer = self._column_map.get(index.column(), lambda p: None)
            return renderer(self._data[index.row()])

        def on_text_alignment():
            return Qt.AlignCenter

        def on_background():
            return QColor(Qt.white) if index.row() % 2 == 0 else self._lightgray

        return {
            Qt.DisplayRole: on_display,
            Qt.TextAlignmentRole: on_text_alignment,
            Qt.BackgroundRole: on_background,
        }.get(role, lambda: None)()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header[section] if 0 <= section < len(self._header) else None
        elif role == Qt.TextAlignmentRole and orientation == Qt.Horizontal:
            return Qt.AlignCenter
        return super().headerData(section, orientation, role)

    def update_row(self, index):
        self.dataChanged.emit(self.index(index, 0),
                              self.index(index, len(self._header) - 1))

    def begin_append_row(self):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))

    def end_append_row(self):
        self.endInsertRows()


class ProcessTableModel(TableModel):
    _column_map = {
        0: lambda process: process.id,
        1: lambda process: process.__class__.__name__,
        2: lambda process: str(process.state),
        3: lambda process: process.remaining_time,
    }


class ProcessQueueModel(TableModel):
    _column_map = {
        0: lambda process: str(process),
    }

    def update_row(self, index):
        idx = self.index(index, 0)
        self.dataChanged.emit(idx, idx)


class LogTableModel(TableModel):
    _column_map = {
        0: lambda _log: _log.time,
        1: lambda _log: str(_log.process),
        2: lambda _log: str(_log.transition.before()),
        3: lambda _log: str(_log.transition.after()),
        4: lambda _log: _log.transition.description(),
    }
