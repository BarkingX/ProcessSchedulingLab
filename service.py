class SimulationService:
    def start_simulation(self, model):
        model.is_running = True
        # 在这里可以添加开始模拟程序的执行的业务逻辑

    def pause_simulation(self, model):
        model.is_running = False
        # 在这里可以添加暂停模拟程序的执行的业务逻辑

    def reset_simulation(self, model):
        # 在这里可以添加重置模拟程序的状态的业务逻辑
        pass