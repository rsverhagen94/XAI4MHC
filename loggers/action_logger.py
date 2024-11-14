from matrx.logger.logger import GridWorldLogger
from matrx.grid_world import GridWorld

class action_logger(GridWorldLogger):
    """ logs all executed actions for both robots, their locations, and task completeness during each tick of the task """

    def __init__(self, save_path="", file_name_prefix="", file_extension=".csv", delimiter=";"):
        super().__init__(save_path=save_path, file_name=file_name_prefix, file_extension=file_extension,
                         delimiter=delimiter, log_strategy=1)

    def log(self, grid_world, agent_data):
        log_data = {}
        log_data['completeness'] = grid_world.simulation_goal.progress(grid_world)
        for agent_id, agent_body in grid_world.registered_agents.items():
            if 'titus' in agent_id or 'brutus' in agent_id:
                log_data[agent_id + '_action'] = agent_body.current_action
                log_data[agent_id + '_location'] = agent_body.location
        return log_data