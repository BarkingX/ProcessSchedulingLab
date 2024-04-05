import tkinter as tk
from tkinter import ttk

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.processes = []
        self.current_time = 0

        # 创建框架
        self.input_frame = tk.Frame(root)
        self.input_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        # 创建下拉菜单
        options = ["Random Process", "Producer", "Consumer"]
        self.dropdown_var = tk.StringVar(self.input_frame)
        self.dropdown_var.set(options[0])  # 默认选择第一个选项
        self.dropdown = tk.OptionMenu(self.input_frame, self.dropdown_var, *options)
        self.dropdown.pack(side='left', padx=10, pady=10)
        # 输入框接收burst_time
        self.burst_time_entry = tk.Entry(self.input_frame)
        self.burst_time_entry.pack(side='left', padx=10, pady=10)
        # 创建进程按钮
        self.create_process_button = tk.Button(self.input_frame, text="Create Process", command=self.create_process)
        self.create_process_button.pack(side='left', padx=10, pady=10)

        # 状态显示
        self.status_frame = tk.Frame(root)
        self.status_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.current_time_label = tk.Label(self.status_frame, text="Current Time: 0")
        self.current_time_label.pack(side='left', padx=10, pady=10)
        self.current_process_label = tk.Label(self.status_frame, text="Current Process ID: None")
        self.current_process_label.pack(side='left', padx=10, pady=10)
        self.item_count_label = tk.Label(self.status_frame, text="Item Count: 0")
        self.item_count_label.pack(side='left', padx=10, pady=10)


        # 显示区域
        columns = ("ID", "State", "Remaining Time", "Type")
        self.process_status_table = ttk.Treeview(root, columns=columns, show='headings')
        self.process_status_table.heading("#1", text="ID")
        self.process_status_table.heading("#2", text="State")
        self.process_status_table.heading("#3", text="Remaining Time")
        self.process_status_table.heading("#4", text="Type")
        self.process_status_table.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # 列表
        self.queue_frame = tk.Frame(root)
        self.queue_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        runnable_frame = tk.Frame(self.queue_frame)
        runnable_frame.pack(side='left')
        self.runnable_label = tk.Label(runnable_frame, text="Runnable Processes")
        self.runnable_label.pack()
        self.runnable_processes_list = tk.Listbox(runnable_frame, height=10, width=20)
        self.runnable_processes_list.pack()
        blocked_frame = tk.Frame(self.queue_frame)
        blocked_frame.pack(side='left')
        self.blocked_label = tk.Label(blocked_frame, text="Blocked Processes")
        self.blocked_label.pack()
        self.blocked_processes_list = tk.Listbox(blocked_frame, height=10, width=20)
        self.blocked_processes_list.pack()

        # 控制按钮
        self.control_buttons_frame = tk.Frame(root)
        self.control_buttons_frame.grid(row=3, column=2, padx=10, pady=10)
        self.pause_resume_button = tk.Button(self.control_buttons_frame, text="Pause/Resume", command=self.pause_resume_simulation)
        self.pause_resume_button.pack()
        self.next_time_button = tk.Button(self.control_buttons_frame, text="Next Time", command=self.next_time)
        self.next_time_button.pack()
        self.reset_button = tk.Button(self.control_buttons_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack()

        # 日志
        self.show_log_button = tk.Button(root, text="Show Log", command=self.show_log_window)
        self.show_log_button.grid(row=4, column=0, padx=10, pady=10)




    def create_process(self):
        pass
        # burst_time = int(self.burst_time_entry.get())
        # process_type = self.dropdown_var.get()
        # new_process = Process(burst_time, process_type)
        # self.processes.append(new_process)
        # 更新显示区域中的内容

    def show_log_window(self):
        # 弹出窗口展示运行记录表
        pass

    def pause_resume_simulation(self):
        # 暂停/恢复模拟程序
        pass

    def next_time(self):
        # 下一个程序时间
        pass

    def reset_simulation(self):
        # 重置模拟程序
        pass

