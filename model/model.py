import re
from collections import deque

from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel

from simulation.model.process import Producer, Consumer


class SchedulingModel:
    _producer_pattern = re.compile('producer', re.I)

    def __init__(self):
        self.inventory = []
        self.processes = []
        self.runnables = deque()
        self.blockeds = deque()

    def item_count(self):
        return len(self.inventory)

    def add_process_by_type(self, process_type, **kwargs):
        (self.add_producer if re.match('producer', process_type, re.I)
         else self.add_consumer)(**kwargs)

    def add_producer(self, **kwargs):
        self.add_process(Producer(self.inventory.append, **kwargs))

    def add_consumer(self, **kwargs):
        self.add_process(Consumer(self.inventory.pop, **kwargs))

    def add_process(self, process):
        self.processes.append(process)
        self.runnables.append(process)


class TableModel(QAbstractTableModel):
    _column_map = None

    def __init__(self, parent, header, data):
        super().__init__(parent)
        self._header = header
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._header)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            process = self._data[index.row()]
            return self._column_map.get(index.column(), lambda p: None)(process)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header[section] if 0 <= section < len(self._header) else None
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
        self.dataChanged.emit((i := self.index(index, 0)), i)


class LogModel(TableModel):
    _column_map = {
        0: lambda _log: _log.time,
        1: lambda _log: _log.process,
        2: lambda _log: _log.transition.before(),
        3: lambda _log: _log.transition.after(),
        4: lambda _log: _log.transition.description(),
    }
