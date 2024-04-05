import tkinter as tk

from simulation.ui import SimulationApp

# 创建主窗口
root = tk.Tk()
root.title("Process Simulation")

# 创建程序实例
app = SimulationApp(root)

# 运行主循环
root.mainloop()