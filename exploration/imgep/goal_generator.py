import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
from exploration.imgep.features import Features
class GoalGenerator(Features):
    def __init__(self,
                 num_bank:int,
                 modules:list):
        super().__init__()
        self.num_bank = num_bank
        self.k_time = 0
        self.k_miss = 0
        self.modules = modules
    def __call__(self,H:History, module:str)->np.ndarray:
        assert module in self.modules, f"module {module} unknown"
        stats_ = H.memory_perf
        stat = self.data2feature(stats_, module)
        print("module", module)
        print("stat shape", stat.shape)
        if module=="time":
            times = np.random.randint(.6*stat.min(axis=1), 4*stat.max(axis=1))
            return times
        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:
            min_ = stat.min(axis=1)
            max_ = stat.max(axis=1)
            __target = np.random.uniform(.6*min_,1.5*max_)
            return miss_target
        elif type(module)==dict: 
            if module["type"] in ["miss_ratios"] + ["time"] +["time_diff"]:
                min_ = min(stat)
                max_ = max(stat)
                out = np.random.randint(0.6*min_,4.0*max_,(1,))
                return out
            if module["type"]=="miss_ratios_detailled":
                min_ = np.min(stat)
                max_ = np.max(stat)
                out = np.random.randint(0.6*min_,4.0*max_,(1,))
                return out

        elif module in [f"miss_count_bank_{j}" for j in range(self.num_bank)]:
            min_ = .6*stat.min(axis=1)
            max_ = stat.max(axis=1)
            out = np.random.randint(0.6*min_,4.0*max_,(1,))
            return out
        elif module in [f"diff_ratios_bank_{j}" for j in range(self.num_bank)]:
            min_ = stat.min(axis=1)
            max_ = stat.max(axis=1)
            min_ = (1-np.sign(minmiss)*0.4)*minmiss
            out = np.random.uniform(min_,max_)
            return out
