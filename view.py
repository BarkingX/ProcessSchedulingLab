from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QComboBox, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem
)

from simulation.model.process import Process


class SimulationView(QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 输入框架
        input_frame = QWidget()
        input_layout = QHBoxLayout()
        input_frame.setLayout(input_layout)
        main_layout.addWidget(input_frame)
        options = [cls.__name__ for cls in Process.__subclasses__()]
        self.dropdown = QComboBox()
        self.dropdown.addItems(options)
        input_layout.addWidget(self.dropdown)
        self.burst_time_entry = QLineEdit('5')
        input_layout.addWidget(self.burst_time_entry)
        self.create_process_button = QPushButton('Create Process')
        input_layout.addWidget(self.create_process_button)

        # 状态显示
        self.status_frame = QWidget()
        status_layout = QHBoxLayout()
        self.status_frame.setLayout(status_layout)
        main_layout.addWidget(self.status_frame)
        self.current_time_label = QLabel('Current Time: 0')
        status_layout.addWidget(self.current_time_label)
        self.current_process_label = QLabel('Current Process ID: None')
        status_layout.addWidget(self.current_process_label)
        self.item_count_label = QLabel('Item Count: 0')
        status_layout.addWidget(self.item_count_label)

        # 显示区域
        self.process_status_table = QTableWidget()
        self.process_status_table.setColumnCount(4)
        self.process_status_table.setHorizontalHeaderLabels(['ID', 'Type', 'State', 'Remaining Time'])
        main_layout.addWidget(self.process_status_table)

        # 列表
        self.queue_frame = QWidget()
        queue_layout = QHBoxLayout()
        self.queue_frame.setLayout(queue_layout)
        main_layout.addWidget(self.queue_frame)
        runnable_frame = QWidget()
        queue_layout.addWidget(runnable_frame)
        self.runnable_label = QLabel('Runnable Processes')
        queue_layout.addWidget(self.runnable_label)
        self.runnable_processes_text = QTextEdit()
        self.runnable_processes_text.setReadOnly(True)
        queue_layout.addWidget(self.runnable_processes_text)
        blocked_frame = QWidget()
        queue_layout.addWidget(blocked_frame)
        self.blocked_label = QLabel('Blocked Processes')
        queue_layout.addWidget(self.blocked_label)
        self.blocked_processes_text = QTextEdit()
        self.blocked_processes_text.setReadOnly(True)
        queue_layout.addWidget(self.blocked_processes_text)

        # 控制按钮
        self.buttons_frame = QWidget()
        buttons_layout = QVBoxLayout()
        self.buttons_frame.setLayout(buttons_layout)
        main_layout.addWidget(self.buttons_frame)
        self.show_log_button = QPushButton('Show Log')
        buttons_layout.addWidget(self.show_log_button)
        self.pause_resume_button = QPushButton('Pause/Resume')
        buttons_layout.addWidget(self.pause_resume_button)
        self.next_turn_button = QPushButton('Next Time')
        buttons_layout.addWidget(self.next_turn_button)
        self.reset_button = QPushButton('Reset')
        buttons_layout.addWidget(self.reset_button)

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
        return self.dropdown.currentText(), self.burst_time_entry.text()

    def set_create_process(self, callback):
        self.create_process_button.clicked.connect(callback)
        return self

    def set_show_log(self, callback):
        self.show_log_button.clicked.connect(callback)
        return self

    def set_pause_resume(self, callback):
        self.pause_resume_button.clicked.connect(callback)
        return self

    def set_next_turn(self, callback):
        self.next_turn_button.clicked.connect(callback)
        return self

    def set_reset_simulation(self, callback):
        self.reset_button.clicked.connect(callback)
        return self

