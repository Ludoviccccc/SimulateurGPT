import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
class IR:
    def __init__(self,modules,history:History):
        self.history = history
        self.modules = modules
    def __call__(self,
                 parameter:dict[list], 
                 observation:dict[list],
                 goal:np.ndarray,
                 module):
        print("module",module)
        def feature(module,observation):
            if type(module)==dict:
                if module["type"] == "time":
                    core = module["core"]
                    single = module["single"]
                    #bank = module["bank"]
            pass
        print("goal", goal)
        print("observation",observation)
        exit()
