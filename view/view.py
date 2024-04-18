from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIntValidator
from PySide6.QtWidgets import *

from simulation.strings import Strings, Templates
from simulation.model.process import Process


class SchedulingView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Strings.WINDOW_TITLE)
        self.resize(QSize(900, 600))

    def setup(self):
        self._setup_main_widget()
        self._setup_tool_bar()
        self._setup_log_dialog()
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

        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.addAction(self.pause_resume_action)
        toolbar.addAction(self.next_turn_action)
        toolbar.addAction(self.reset_action)
        toolbar.addAction(self.show_log_table_action)
        self.addToolBar(toolbar)

    def _setup_log_dialog(self):
        self.log_table_dialog = QDialog(self)
        self.log_table_dialog.view = QTableView(self.log_table_dialog)
        self.log_table_dialog.view.horizontalHeader().setStretchLastSection(True)
        layout = QVBoxLayout(self.log_table_dialog)
        layout.addWidget(self.log_table_dialog.view)
        self.log_table_dialog.setWindowTitle(Strings.LOG_DIALOG_TITLE)
        self.log_table_dialog.setLayout(layout)
        self.log_table_dialog.resize(QSize(720, 480))

    def _setup_input_widget(self):
        input_widget = QWidget(self.main_widget)
        input_layout = QHBoxLayout(input_widget)

        self.ptype_dropdown = QComboBox(input_widget)
        self.ptype_dropdown.addItems([cls.__name__ for cls in Process.__subclasses__()])
        self.burst_time_input = QLineEdit(input_widget)
        self.burst_time_input.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed,
                                                        QSizePolicy.Policy.Fixed))
        self.burst_time_input.setPlaceholderText(Strings.BURST_TIME_INPUT_TIP)
        self.burst_time_input.setValidator(QIntValidator(0, 100, self.burst_time_input))
        self.create_process_button = QPushButton(Strings.CREATE_PROCESS, input_widget)

        input_layout.addWidget(self.ptype_dropdown)
        input_layout.addWidget(self.burst_time_input)
        input_layout.addWidget(self.create_process_button)
        input_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding))
        self.main_layout.addWidget(input_widget)

    def _setup_process_status_widget(self):
        def _setup_labels(widget, layout):
            titles = [Strings.PROCESS_TABLE, Strings.RUNNABLE_QUEUE,
                      Strings.BLOCKED_QUEUE]
            for col, title in enumerate(titles):
                label = QLabel(title, widget)
                layout.addWidget(label, 0, col, alignment=Qt.AlignmentFlag.AlignHCenter)

        def _setup_views(widget, layout):
            def _view_alignment(_col):
                return (Qt.AlignmentFlag.AlignRight if _col > 0 else
                        Qt.AlignmentFlag.AlignTop & Qt.AlignmentFlag.AlignBottom)

            def _non_editable_listview(parent):
                list_view = QListView(parent)
                list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
                return list_view

            self.process_tableview = QTableView(widget)
            self.process_tableview.horizontalHeader().setStretchLastSection(True)
            self.runnable_listview = _non_editable_listview(widget)
            self.blocked_listview = _non_editable_listview(widget)
            views = [self.process_tableview,
                     self.runnable_listview, self.blocked_listview]

            for (col, view), weight in zip(enumerate(views), [4, 1, 1]):
                layout.addWidget(view, 1, col, alignment=_view_alignment(col))
                layout.setColumnStretch(col, weight)

        process_status_widget = QWidget(self.main_widget)
        process_status_layout = QGridLayout(process_status_widget)
        _setup_labels(process_status_widget, process_status_layout)
        _setup_views(process_status_widget, process_status_layout)
        self.main_layout.addWidget(process_status_widget)

    def _setup_status_bar(self):
        def _add_permanent_label(text):
            label = QLabel(text)
            status_bar.addPermanentWidget(label)
            return label

        status_bar = QStatusBar(self)
        self.progress_bar = QProgressBar(status_bar)
        self.progress_bar.setMaximumWidth(180)
        self.progress_bar.setVisible(False)
        status_bar.addWidget(self.progress_bar)
        self.current_time_label = _add_permanent_label(Templates.CURRENT_TIME.format(0))
        self.current_process_label = _add_permanent_label(
            Templates.CURRENT_PROCESS_ID.format('None'))
        self.item_count_label = _add_permanent_label(Templates.ITEM_COUNT.format(0))

        self.setStatusBar(status_bar)

    def start_progress(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)

    def stop_progress(self):
        self.progress_bar.setVisible(False)

    def process_type_and_burst_time(self):
        return self.ptype_dropdown.currentText(), self.burst_time_input.text()

    def update_views(self):
        self.process_tableview.viewport().update()
        self.runnable_listview.viewport().update()
        self.blocked_listview.viewport().update()

    def update_labels(self, time, process_id, item_count):
        self.current_time_label.setText(Templates.CURRENT_TIME.format(time))
        self.current_process_label.setText(
            Templates.CURRENT_PROCESS_ID.format(process_id))
        self.item_count_label.setText(Templates.ITEM_COUNT.format(item_count))

    def set_create_process_callback(self, callback):
        self.create_process_button.clicked.connect(callback)

    def set_process_tablemodel(self, model):
        self.process_tableview.setModel(model)

    def set_runnable_listmodel(self, model):
        self.runnable_listview.setModel(model)

    def set_blocked_listmodel(self, model):
        self.blocked_listview.setModel(model)

    def set_log_tablemodel(self, model):
        self.log_table_dialog.view.setModel(model)

    def set_show_log_callback(self, callback):
        self.show_log_table_action.triggered.connect(callback)

    def set_next_turn_callback(self, callback):
        self.next_turn_action.triggered.connect(callback)

    def set_pause_resume_callback(self, callback):
        self.pause_resume_action.triggered.connect(callback)

    def set_reset_simulation_callback(self, callback):
        self.reset_action.triggered.connect(callback)
