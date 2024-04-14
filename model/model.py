from collections import deque

from PySide6.QtCore import Qt, QModelIndex, QAbstractTableModel
from PySide6.QtGui import QColor

from simulation.model.process import Producer, Consumer, producer_pattern


class SchedulingModel:
    def __init__(self):
        self.inventory = []
        self.processes = []
        self.runnables = deque()
        self.blockeds = deque()

    def item_count(self):
        return len(self.inventory)

    def add_process_by_type(self, process_type, **kwargs):
        (self.add_new_producer if producer_pattern.match(process_type)
         else self.add_new_consumer)(**kwargs)

    def add_new_producer(self, **kwargs):
        self.add_new_process(Producer(self.inventory.append, **kwargs))

    def add_new_consumer(self, **kwargs):
        self.add_new_process(Consumer(self.inventory.pop, **kwargs))

    def add_new_process(self, process):
        self.processes.append(process)
        self.runnables.append(process)

    def clear_all(self):
        self.processes.clear()
        self.runnables.clear()
        self.blockeds.clear()
        self.inventory.clear()


class TableModel(QAbstractTableModel):
    _column_map = None
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
            render = self._column_map.get(index.column(), lambda p: None)
            return render(self._data[index.row()])

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
        self.dataChanged.emit((i := self.index(index, 0)), i)


class LogTableModel(TableModel):
    _column_map = {
        0: lambda _log: _log.time,
        1: lambda _log: str(_log.process),
        2: lambda _log: str(_log.transition.before()),
        3: lambda _log: str(_log.transition.after()),
        4: lambda _log: _log.transition.description(),
    }
