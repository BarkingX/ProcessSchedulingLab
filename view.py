from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *

from simulation.strings import Strings, Templates
from simulation.model.process import Process


def _non_editable_listview(parent):
    list_view = QListView(parent)
    list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    return list_view


class SchedulingView(QMainWindow):
    def __init__(self):
        super().__init__()
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        self.pause_resume_action = QAction(Strings.PAUSE_RESUME.split('/')[-1], self)
        self.pause_resume_action.setShortcut(Strings.PAUSE_RESUME_KEY)
        self.next_turn_action = QAction(Strings.NEXT_TURN, self)
        self.next_turn_action.setShortcut(Strings.NEXT_TURN_KEY)
        self.reset_action = QAction(Strings.RESET, self)
        self.reset_action.setShortcut(Strings.RESET_KEY)
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
        self.create_process_button = QPushButton(Strings.CREATE_PROCESS, input_widget)
        self.show_log_button = QPushButton(Strings.SHOW_LOG, input_widget)
        input_layout.addWidget(self.ptype_dropdown)
        input_layout.addWidget(self.burst_time_input)
        input_layout.addWidget(self.create_process_button)
        input_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding))
        input_layout.addWidget(self.show_log_button)

        process_status_widget = QWidget(main_widget)
        process_table_title = QLabel(Strings.PROCESS, process_status_widget)
        runnable_queue_title = QLabel(Strings.RUNNABLE_QUEUE, process_status_widget)
        blocked_queue_title = QLabel(Strings.BLOCKED_QUEUE, process_status_widget)
        self.process_table_view = QTableView(process_status_widget)
        self.process_table_view.horizontalHeader().setStretchLastSection(True)

        self.runnable_queue_view = _non_editable_listview(process_status_widget)
        self.blocked_queue_view = _non_editable_listview(process_status_widget)

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

        self.current_time_label = QLabel(Templates.CURRENT_TIME.format(0))
        self.current_process_label = QLabel(Templates.CURRENT_PROCESS_ID.format('None'))
        self.item_count_label = QLabel(Templates.ITEM_COUNT.format(0))
        status_bar = QStatusBar(self)
        status_bar.addPermanentWidget(self.current_time_label)
        status_bar.addPermanentWidget(self.current_process_label)
        status_bar.addPermanentWidget(self.item_count_label)
        self.setStatusBar(status_bar)

        self.setWindowTitle(Strings.WINDOW_TITLE)
        self.setCentralWidget(main_widget)

    def process_type_and_burst_time(self):
        return self.ptype_dropdown.currentText(), self.burst_time_input.text()

    def update_labels(self, time, process_id, item_count):
        self.current_time_label.setText(Templates.CURRENT_TIME.format(time))
        self.current_process_label.setText(
            Templates.CURRENT_PROCESS_ID.format(process_id))
        self.item_count_label.setText(Templates.ITEM_COUNT.format(item_count))

    def set_create_process(self, callback):
        self.create_process_button.clicked.connect(callback)

    def set_process_table_model(self, model):
        self.process_table_view.setModel(model)

    def set_runnable_model(self, model):
        self.runnable_queue_view.setModel(model)

    def set_blocked_model(self, model):
        self.blocked_queue_view.setModel(model)

    def set_show_log(self, callback):
        self.show_log_button.clicked.connect(callback)

    def set_next_turn(self, callback):
        self.next_turn_action.triggered.connect(callback)

    def set_pause_resume(self, callback):
        self.pause_resume_action.triggered.connect(callback)

    def set_reset_simulation(self, callback):
        self.reset_action.triggered.connect(callback)
