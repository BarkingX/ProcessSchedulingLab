from collections import deque
from typing import List, Deque

from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PySide6.QtGui import QColor

from simulation.model import Process
from simulation.model.process import ProcessCreator
from simulation.util import Item


class SchedulingModel:
    def __init__(self):
        self.inventory: List[Item] = []
        self.processes: List[Process] = []
        self.runnables: Deque[Process] = deque()
        self.blockeds: Deque[Process] = deque()
        self._pfactory = ProcessCreator(self.inventory)

    @property
    def item_count(self):
        return len(self.inventory)

    @property
    def last_process(self):
        return self.processes[-1]

    def add_new_process(self, *args):
        process = self._pfactory.create_process(*args)
        self.processes.append(process)
        self.runnables.append(process)

    def enqueue_runnable(self, p):
        self.runnables.append(p)

    def dequeue_runnables(self):
        return self.runnables.popleft()

    def has_runnable(self):
        return bool(len(self.runnables))

    def enqueue_blocked(self, p):
        self.blockeds.append(p)

    def dequeue_blockeds(self):
        return self.blockeds.popleft()

    def has_blocked(self):
        return bool(len(self.blockeds))

    def process_index(self, p):
        try:
            return self.processes.index(p)
        except ValueError:
            return 0

    def reset(self):
        for collection in [self.processes, self.runnables, self.inventory, self.blockeds]:
            collection.clear()


class TableModel(QAbstractTableModel):
    _column_map = {}
    _lightgray = QColor(230, 230, 230)

    def __init__(self, parent, header, data):
        super().__init__(parent)
        self._header = header
        self._data = data
        self._role_method_map = {
            Qt.DisplayRole: self._on_display,
            Qt.TextAlignmentRole: self._on_text_alignment,
            Qt.BackgroundRole: self._on_background
        }

    def _on_display(self, index):
        renderer = self._column_map.get(index.column(), lambda p: None)
        return renderer(self._data[index.row()])

    def _on_text_alignment(self, index):
        return Qt.AlignCenter

    def _on_background(self, index):
        return QColor(Qt.white) if index.row() % 2 == 0 else self._lightgray

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        return self._role_method_map.get(role, lambda _: None)(index)

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
