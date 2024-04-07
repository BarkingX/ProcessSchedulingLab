from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import *

from simulation import strings
from simulation.model.process import Process


def _update_queue(model, queue):
    model.clear()
    for p in queue:
        model.appendRow(QStandardItem(p))


def _non_editable_listview(parent):
    list_view = QListView(parent)
    list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    model = QStandardItemModel(list_view)
    list_view.setModel(model)
    return list_view, model


class SimulationView(QMainWindow):
    def __init__(self):
        super().__init__()
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.pause_resume_action = QAction(strings.PAUSE_RESUME, self)
        self.pause_resume_action.setShortcut(strings.PAUSE_RESUME_KEY)
        self.next_turn_action = QAction(strings.NEXT_TURN, self)
        self.next_turn_action.setShortcut(strings.NEXT_TURN_KEY)
        self.reset_action = QAction(strings.RESET, self)
        self.reset_action.setShortcut(strings.RESET_KEY)
        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.addAction(self.pause_resume_action)
        toolbar.addAction(self.next_turn_action)
        toolbar.addAction(self.reset_action)
        self.addToolBar(toolbar)

        input_widget = QWidget(main_widget)
        input_layout = QHBoxLayout(input_widget)
        main_layout.addWidget(input_widget)
        self.ptype_dropdown = QComboBox(input_widget)
        self.ptype_dropdown.addItems([cls.__name__ for cls in Process.__subclasses__()])
        self.burst_time_input = QLineEdit(input_widget)
        self.burst_time_input.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                        QSizePolicy.Policy.Fixed))
        self.create_process_button = QPushButton(strings.CREATE_PROCESS, input_widget)
        self.show_log_button = QPushButton(strings.SHOW_LOG, input_widget)
        input_layout.addWidget(self.ptype_dropdown)
        input_layout.addWidget(self.burst_time_input)
        input_layout.addWidget(self.create_process_button)
        input_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding))
        input_layout.addWidget(self.show_log_button)

        process_status_widget = QWidget(main_widget)
        process_table_title = QLabel(strings.PROCESS, process_status_widget)
        runnable_queue_title = QLabel(strings.RUNNABLE_QUEUE, process_status_widget)
        blocked_queue_title = QLabel(strings.BLOCKED_QUEUE, process_status_widget)
        self.process_table_view = QTableWidget(process_status_widget)
        self.process_table_view.setColumnCount(4)
        self.process_table_view.setHorizontalHeaderLabels(
            ['ID', 'Type', 'State', 'Remaining Time'])
        self.process_table_view.horizontalHeader().setStretchLastSection(True)

        (self.runnable_queue_view,
         self.runnable_queue_model) = _non_editable_listview(process_status_widget)
        (self.blocked_queue_view,
         self.blocked_queue_model) = _non_editable_listview(process_status_widget)

        hcenter = Qt.AlignmentFlag.AlignHCenter
        right = Qt.AlignmentFlag.AlignRight
        process_status_layout = QGridLayout(process_status_widget)
        process_status_layout.addWidget(process_table_title, 0, 0, alignment=hcenter)
        process_status_layout.addWidget(runnable_queue_title, 0, 1, alignment=hcenter)
        process_status_layout.addWidget(blocked_queue_title, 0, 2, alignment=hcenter)
        process_status_layout.addWidget(self.process_table_view, 1, 0)
        process_status_layout.addWidget(self.runnable_queue_view, 1, 1, alignment=right)
        process_status_layout.addWidget(self.blocked_queue_view, 1, 2, alignment=right)
        process_status_layout.setColumnStretch(0, 4)
        process_status_layout.setColumnStretch(1, 1)
        process_status_layout.setColumnStretch(2, 1)
        process_status_layout.setSpacing(10)
        process_status_widget.setLayout(process_status_layout)
        main_layout.addWidget(process_status_widget)

        self.current_time_label = QLabel(strings.Templates.CURRENT_TIME.format(0))
        self.current_process_label = QLabel(
            strings.Templates.CURRENT_PROCESS_ID.format('None'))
        self.item_count_label = QLabel(strings.Templates.ITEM_COUNT.format(0))
        status_bar = QStatusBar(self)
        status_bar.addPermanentWidget(self.current_time_label)
        status_bar.addPermanentWidget(self.current_process_label)
        status_bar.addPermanentWidget(self.item_count_label)
        self.setStatusBar(status_bar)

        self.setWindowTitle(strings.WINDOW_TITLE)
        self.setCentralWidget(main_widget)

    def update(self):
        pass

    def update_process_table(self, records):
        records = list(records)
        print(records)
        self.process_table_view.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.process_table_view.setItem(row, col, item)

    def update_runnable_queue(self, runnable_queue):
        _update_queue(self.runnable_queue_model, runnable_queue)

    def update_blocked_queue(self, blocked_queue):
        _update_queue(self.blocked_queue_model, blocked_queue)

    def append_process_table(self, process_info):
        row_position = self.process_table_view.rowCount()
        self.process_table_view.insertRow(row_position)
        for col, value in enumerate(process_info):
            item = QTableWidgetItem(str(value))
            self.process_table_view.setItem(row_position, col, item)

    def update_labels(self, time, process, item_count):
        self.current_time_label.setText(strings.Templates.CURRENT_TIME.format(time))
        self.current_process_label.setText(
            strings.Templates.CURRENT_PROCESS_ID.format(process))
        self.item_count_label.setText(strings.Templates.ITEM_COUNT.format(item_count))

    def process_type_and_burst_time(self):
        return self.ptype_dropdown.currentText(), self.burst_time_input.text()

    def set_create_process(self, callback):
        self.create_process_button.clicked.connect(callback)
        return self

    def set_runnable_model(self, model):
        self.runnable_queue_view.setModel(model)
        return self

    def set_blocked_model(self, model):
        self.blocked_queue_view.setModel(model)
        return self

    def set_show_log(self, callback):
        self.show_log_button.clicked.connect(callback)
        return self

    def set_pause_resume(self, callback):
        self.pause_resume_action.triggered.connect(callback)
        return self

    def set_next_turn(self, callback):
        self.next_turn_action.triggered.connect(callback)
        return self

    def set_reset_simulation(self, callback):
        self.reset_action.triggered.connect(callback)
        return self
