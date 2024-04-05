from simulation.model.model import SimulationModel
from simulation.view import SimulationView


class SimulationController:
    def __init__(self, model: SimulationModel, view: SimulationView, service):
        self.model = model
        self.view = view
        self.service = service

        type, burst_time = view.process_type_and_burst_time()

        view.set_create_process()

    def start_simulation(self):
        self.service.start_simulation(self.model)
        # 在这里可以添加更新视图的逻辑

    def pause_simulation(self):
        self.service.pause_simulation(self.model)
        # 在这里可以添加更新视图的逻辑

    def reset_simulation(self):
        self.service.reset_simulation(self.model)
        # 在这里可以添加更新视图的逻辑
