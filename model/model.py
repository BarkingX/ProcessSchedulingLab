from collections import deque

from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex
from PySide6.QtGui import QStandardItemModel

from simulation.model.process import Producer, Consumer, Process
from simulation.model.scheduler import RoundRobinScheduler, ScheduleHelper
from simulation.util import Timer


class SimulationModel:
    def __init__(self):
        self.inventory = []
        self.processes = []
        self.runnable = deque()
        self.blocked = deque()
        self.timer = Timer(1)
        self.helper = ScheduleHelper(self.timer, lambda: len(self.inventory) > 0)
        self.scheduler = RoundRobinScheduler(self.runnable, self.blocked, self.helper)

    def add_type(self, process_type, **kwargs):
        if 'Producer' == process_type:
            self.add_producer(**kwargs)
        elif 'Consumer' == process_type:
            self.add_consumer(**kwargs)

    def add_producer(self, **kwargs):
        self.add_process(self.new_producer(**kwargs))

    def add_consumer(self, **kwargs):
        self.add_process(self.new_consumer(**kwargs))

    def add_process(self, process):
        self.processes.append(process)
        self.runnable.append(process)

    def new_type(self, process_type, **kwargs):
        if 'Producer' == process_type:
            return self.new_producer(**kwargs)
        elif 'Consumer' == process_type:
            return self.new_consumer(**kwargs)

    def new_producer(self, **kwargs):
        return Producer(self.inventory.append, **kwargs)

    def new_consumer(self, **kwargs):
        return Consumer(self.inventory.pop, **kwargs)


class ProcessTableModel(QAbstractItemModel):
    def __init__(self, parent, header, model):
        super().__init__(parent)
        self._parent = parent
        self._header = header
        self._data = model

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 4  # Assuming 4 attributes in Process class

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            process = self._data[index.row()]
            if index.column() == 0:
                return process.id
            elif index.column() == 1:
                return process.__class__.__name__
            elif index.column() == 2:
                return str(process.state)
            elif index.column() == 3:
                return process.remaining_time
        return None  # Return None for other roles or unsupported columns

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header[section] if 0 <= section < len(self._header) else None
        return super().headerData(section, orientation, role)

    def index(self, row, column, parent=QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def begin_append_row(self):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))

    def end_append_row(self):
        self.endInsertRows()

    def parent(self):
        return self._parent


class ProcessQueueModel(QAbstractItemModel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self._parent = parent
        self._data = data

    def begin_append_row(self):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))

    def end_append_row(self):
        self.endInsertRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            process = self._data[index.row()]
            if index.column() == 0:
                return str(process)
        return None

    def index(self, row, column, parent=QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def parent(self):
        return self._parent
