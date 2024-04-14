from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *

from simulation.strings import Strings, Templates
from simulation.model.process import Process


def _non_editable_listview(parent):
    list_view = QListView(parent)
    list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    return list_view


def _table_dialog(parent):
    log_dialog = QDialog(parent)
    log_dialog.view = QTableView(log_dialog)
    log_dialog.view.horizontalHeader().setStretchLastSection(True)
    layout = QVBoxLayout(log_dialog)
    layout.addWidget(log_dialog.view)
    log_dialog.setWindowTitle(Strings.LOG_DIALOG_TITLE)
    log_dialog.setLayout(layout)
    log_dialog.resize(600, 400)
    return log_dialog


def _setup_labels(widget, layout):
    titles = [Strings.PROCESS, Strings.RUNNABLE_QUEUE, Strings.BLOCKED_QUEUE]
    for col, title in enumerate(titles):
        label = QLabel(title, widget)
        layout.addWidget(label, 0, col, alignment=Qt.AlignmentFlag.AlignHCenter)


class SchedulingView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Strings.WINDOW_TITLE)

    def setup(self):
        self._setup_main_widget()
        self._setup_tool_bar()
        self._setup_input_widget()
        self._setup_process_status_widget()
        self._setup_status_bar()

    def _setup_main_widget(self):
        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)

    def _setup_tool_bar(self):
        self.pause_resume_action = QAction(Strings.RESUME, self)
        self.pause_resume_action.setShortcut(Strings.PAUSE_RESUME_KEY)
        self.next_turn_action = QAction(Strings.NEXT_TURN, self)
        self.next_turn_action.setShortcut(Strings.NEXT_TURN_KEY)
        self.reset_action = QAction(Strings.RESET, self)
        self.reset_action.setShortcut(Strings.RESET_KEY)
        self.show_log_table_action = QAction(Strings.SHOW_LOG, self)
        self.show_log_table_action.setShortcut(Strings.SHOW_LOG_KEY)
        self.log_table_dialog = _table_dialog(self)
        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.addAction(self.pause_resume_action)
        toolbar.addAction(self.next_turn_action)
        toolbar.addAction(self.reset_action)
        toolbar.addAction(self.show_log_table_action)
        self.addToolBar(toolbar)

    def _setup_input_widget(self):
        input_widget = QWidget(self.main_widget)
        input_layout = QHBoxLayout(input_widget)
        self.ptype_dropdown = QComboBox(input_widget)
        self.ptype_dropdown.addItems([cls.__name__ for cls in Process.__subclasses__()])
        self.burst_time_input = QLineEdit(input_widget)
        self.burst_time_input.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.create_process_button = QPushButton(Strings.CREATE_PROCESS, input_widget)
        input_layout.addWidget(self.ptype_dropdown)
        input_layout.addWidget(self.burst_time_input)
        input_layout.addWidget(self.create_process_button)
        input_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding))
        self.main_layout.addWidget(input_widget)

    def _setup_process_status_widget(self):
        process_status_widget = QWidget(self.main_widget)
        process_status_layout = QGridLayout(process_status_widget)
        _setup_labels(process_status_widget, process_status_layout)
        self._setup_views(process_status_widget, process_status_layout)
        self.main_layout.addWidget(process_status_widget)

    def _setup_views(self, widget, layout):
        def _view_alignment(_col):
            return (Qt.AlignmentFlag.AlignRight if _col > 0 else
                    Qt.AlignmentFlag.AlignTop & Qt.AlignmentFlag.AlignBottom)

        self.process_table_view = QTableView(widget)
        self.process_table_view.horizontalHeader().setStretchLastSection(True)
        self.runnable_queue_view = _non_editable_listview(widget)
        self.blocked_queue_view = _non_editable_listview(widget)
        views = [self.process_table_view,
                 self.runnable_queue_view, self.blocked_queue_view]

        for (col, view), weight in zip(enumerate(views), [4, 1, 1]):
            layout.addWidget(view, 1, col, alignment=_view_alignment(col))
            layout.setColumnStretch(col, weight)

    def _setup_status_bar(self):
        status_bar = QStatusBar(self)
        self.current_time_label = QLabel(Templates.CURRENT_TIME.format(0))
        self.current_process_label = QLabel(Templates.CURRENT_PROCESS_ID.format('None'))
        self.item_count_label = QLabel(Templates.ITEM_COUNT.format(0))
        status_bar.addPermanentWidget(self.current_time_label)
        status_bar.addPermanentWidget(self.current_process_label)
        status_bar.addPermanentWidget(self.item_count_label)
        self.setStatusBar(status_bar)

    def process_type_and_burst_time(self):
        return self.ptype_dropdown.currentText(), self.burst_time_input.text()

    def update_labels(self, time, process_id, item_count):
        self.current_time_label.setText(Templates.CURRENT_TIME.format(time))
        self.current_process_label.setText(
            Templates.CURRENT_PROCESS_ID.format(process_id))
        self.item_count_label.setText(Templates.ITEM_COUNT.format(item_count))

    def set_create_process(self, callback):
        self.create_process_button.clicked.connect(callback)

    def set_process_tablemodel(self, model):
        self.process_table_view.setModel(model)

    def set_runnable_listmodel(self, model):
        self.runnable_queue_view.setModel(model)

    def set_blocked_listmodel(self, model):
        self.blocked_queue_view.setModel(model)

    def set_log_tablemodel(self, model):
        self.log_table_dialog.view.setModel(model)

    def set_show_log(self, callback):
        self.show_log_table_action.triggered.connect(callback)

    def set_next_turn(self, callback):
        self.next_turn_action.triggered.connect(callback)

    def set_pause_resume(self, callback):
        self.pause_resume_action.triggered.connect(callback)

    def set_reset_simulation(self, callback):
        self.reset_action.triggered.connect(callback)

    def update_views(self):
        self.process_table_view.viewport().update()
        self.runnable_queue_view.viewport().update()
        self.blocked_queue_view.viewport().update()
