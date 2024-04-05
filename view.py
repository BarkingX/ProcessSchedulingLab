import tkinter as tk
from tkinter import ttk


class SimulationView:
    def __init__(self, root):
        # 创建框架
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=10)
        # 创建下拉菜单
        options = ['Producer', 'Consumer']
        self.dropdown_var = tk.StringVar(input_frame)
        self.dropdown_var.set(options[0])  # 默认选择第一个选项
        self.dropdown = tk.OptionMenu(input_frame, self.dropdown_var, *options)
        self.dropdown.pack(side='left', padx=10, pady=10)
        # 输入框接收burst_time
        self.burst_time_entry = tk.Entry(input_frame)
        self.burst_time_entry.pack(side='left', padx=10, pady=10)
        # 创建进程按钮
        self.create_process_button = tk.Button(input_frame, text='Create Process')
        self.create_process_button.pack(side='left', padx=10, pady=10)

        # 状态显示
        self.status_frame = tk.Frame(root)
        self.status_frame.pack(padx=10, pady=10)
        self.current_time_label = tk.Label(self.status_frame, text='Current Time: 0')
        self.current_time_label.pack(side='left', padx=10, pady=10)
        self.current_process_label = tk.Label(self.status_frame,
                                              text='Current Process ID: None')
        self.current_process_label.pack(side='left', padx=10, pady=10)
        self.item_count_label = tk.Label(self.status_frame, text='Item Count: 0')
        self.item_count_label.pack(side='left', padx=10, pady=10)

        # 显示区域
        columns = ('ID', 'State', 'Remaining Time', 'Type')
        self.process_status_table = ttk.Treeview(root, columns=columns, show='headings')
        self.process_status_table.heading("#1", text="ID")
        self.process_status_table.heading("#2", text="State")
        self.process_status_table.heading("#3", text="Remaining Time")
        self.process_status_table.heading("#4", text="Type")
        self.process_status_table.pack(padx=10, pady=10)

        # 列表
        self.queue_frame = tk.Frame(root)
        self.queue_frame.pack(side='left', padx=10, pady=10)
        runnable_frame = tk.Frame(self.queue_frame)
        runnable_frame.pack(side='left')
        self.runnable_label = tk.Label(runnable_frame, text='Runnable Processes')
        self.runnable_label.pack()
        self.runnable_processes_list = tk.Listbox(runnable_frame, height=10, width=20)
        self.runnable_processes_list.pack()
        blocked_frame = tk.Frame(self.queue_frame)
        blocked_frame.pack(side='left')
        self.blocked_label = tk.Label(blocked_frame, text='Blocked Processes')
        self.blocked_label.pack()
        self.blocked_processes_list = tk.Listbox(blocked_frame, height=10, width=20)
        self.blocked_processes_list.pack()

        # 控制按钮
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(side='right', padx=10, pady=10)
        self.show_log_button = tk.Button(self.buttons_frame, text='Show Log')
        self.show_log_button.pack(padx=10, pady=10)
        self.pause_resume_button = tk.Button(self.buttons_frame,
                                             text='Pause/Resume')
        self.pause_resume_button.pack(padx=10, pady=10)
        self.next_time_button = tk.Button(self.buttons_frame, text='Next Time')
        self.next_time_button.pack(padx=10, pady=10)
        self.reset_button = tk.Button(self.buttons_frame, text='Reset')
        self.reset_button.pack(padx=10, pady=10)

    @staticmethod
    def update_view(view):
        pass

    def process_type_and_burst_time(self):
        return self.dropdown_var.get(), self.burst_time_entry.get()

    def set_create_process(self, callback):
        return self._set_callback(self.create_process_button, callback)

    def set_show_log(self, callback):
        return self._set_callback(self.show_log_button, callback)

    def set_pause_resume(self, callback):
        return self._set_callback(self.pause_resume_button, callback)

    def set_next_time(self, callback):
        return self._set_callback(self.next_time_button, callback)

    def set_reset_simulation(self, callback):
        return self._set_callback(self.reset_button, callback)

    def _set_callback(self, button, callback):
        button.config(command=callback)
        return self

