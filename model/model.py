from collections import deque

from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex

from simulation.model.process import Producer, Consumer


class SchedulingModel:
    def __init__(self):
        self.inventory = []
        self.processes = []
        self.runnables = deque()
        self.blockeds = deque()

    def item_count(self):
        return len(self.inventory)

    def add_type(self, process_type, **kwargs):
        if 'Producer' == process_type:
            self.add_producer(**kwargs)
        elif 'Consumer' == process_type:
            self.add_consumer(**kwargs)

    def add_producer(self, **kwargs):
        self.add_process(Producer(self.inventory.append, **kwargs))

    def add_consumer(self, **kwargs):
        self.add_process(Consumer(self.inventory.pop, **kwargs))

    def add_process(self, process):
        self.processes.append(process)
        self.runnables.append(process)


class ProcessTableModel(QAbstractItemModel):
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
        return (self.createIndex(row, column)
                if self.hasIndex(row, column, parent) else QModelIndex())

    def update_row(self, index):
        self.dataChanged.emit(self.index(index, 0),
                              self.index(index, len(self._header) - 1))

    def begin_append_row(self):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))

    def end_append_row(self):
        self.endInsertRows()

    def parent(self, child):
        return QModelIndex()


class ProcessQueueModel(QAbstractItemModel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self._data = data

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
        return (self.createIndex(row, column)
                if self.hasIndex(row, column, parent) else QModelIndex())

    def parent(self, child):
        return QModelIndex()

    def update_row(self, index):
        self.dataChanged.emit((i := self.index(index, 0)), i)

    def begin_append_row(self):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))

    def end_append_row(self):
        self.endInsertRows()

