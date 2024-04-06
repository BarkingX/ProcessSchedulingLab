from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QComboBox, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QSizePolicy, QSpacerItem, QStatusBar, QToolBar, QGridLayout, QTableView, QListView
)

from simulation import strings
from simulation.model.process import Process


class SimulationView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(strings.WINDOW_TITLE)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
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
        # input_layout_widget = QWidget(input_widget)
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
        self.runnable_queue_title = QLabel(strings.RUNNABLE_QUEUE, process_status_widget)
        self.blocked_queue_title = QLabel(strings.BLOCKED_QUEUE, process_status_widget)
        self.process_table_view = QTableView(process_status_widget)
        self.runnable_queue_view = QListView(process_status_widget)
        self.blocked_queue_view = QListView(process_status_widget)

        process_status_layout = QGridLayout(process_status_widget)
        process_status_widget.setLayout(process_status_layout)
        process_status_layout.addWidget(self.runnable_queue_title, 0, 1, 1, 1)
        process_status_layout.addWidget(self.blocked_queue_title, 0, 2, 1, 1)
        process_status_layout.addWidget(self.process_table_view, 1, 0, 1, 1)
        process_status_layout.addWidget(self.runnable_queue_view, 1, 1, 1, 1)
        process_status_layout.addWidget(self.blocked_queue_view, 1, 2, 1, 1)
        main_layout.addWidget(process_status_widget)

        self.current_time_label = QLabel('Current Time: 0')
        self.current_process_label = QLabel('Current Process ID: None')
        self.item_count_label = QLabel('Item Count: 0')
        status_bar = QStatusBar(self)
        status_bar.addPermanentWidget(self.current_time_label)
        status_bar.addPermanentWidget(self.current_process_label)
        status_bar.addPermanentWidget(self.item_count_label)
        self.setStatusBar(status_bar)



    def update(self):
        pass

    def update_process_table(self, records):
        self.process_status_table.setRowCount(len(records))
        for row, record in enumerate(records):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.process_status_table.setItem(row, col, item)

    def update_runnable_queue(self):
        # self.runnable_processes_text.
        pass

    def append_process_table(self, process_info):
        row_position = self.process_status_table.rowCount()
        self.process_status_table.insertRow(row_position)
        for col, value in enumerate(process_info):
            item = QTableWidgetItem(str(value))
            self.process_status_table.setItem(row_position, col, item)

    def update_labels(self, time, process, item_count):
        self.current_time_label.setText(f'Current Time: {time}')
        self.current_process_label.setText(f'Current Process ID: {process}')
        self.item_count_label.setText(f'Item Count: {item_count}')

    def process_type_and_burst_time(self):
        return self.ptype_dropdown.currentText(), self.burst_time_input.text()

    def set_create_process(self, callback):
        self.create_process_button.clicked.connect(callback)
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

