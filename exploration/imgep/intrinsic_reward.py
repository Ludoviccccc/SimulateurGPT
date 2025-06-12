import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
from exploration.imgep.goal_generator import GoalGenerator
class IR:
    def __init__(self,modules,
            history:History,
            goal_module:GoalGenerator
            ):
        self.history = history
        self.modules = modules
        self.goal_module = goal_module
        self.progress = {}
    def __call__(self,
                 parameter:dict[list], 
                 observation:dict[list],
                 goal:np.ndarray,
                 module):
        print("module",module)
        def feature(module,observation):
            if type(module)==dict:
                observation_bis = {k:[observation[k]] for k in observation.keys()}
                feature = self.goal_module.data2feature(observation_bis, module)
                if module["type"] in self.progress:
                    self.progress.append(np.linalg.norm(goal-feature))
                elif:
                    self.progress[module["type"]] = [np.linalg.norm(goal-feature)]

