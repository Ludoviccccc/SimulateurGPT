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
        if module=="time":
            times = np.random.randint(.6*stat.min(axis=1), 4*stat.max(axis=1))
            delta = np.random.uniform(.6,4.0,(2,))
            times_together = np.floor(delta*times)
            return np.concatenate((times,times_together))
        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:
            minmiss = .6*stat.min(axis=1)
            maxmiss = 1*stat.max(axis=1)
            miss_target = np.random.uniform(minmiss,maxmiss)
            return miss_target
        elif type(module)==dict: 
            #if module["type"]=="miss_ratios":
            #    minmiss = min(stat)
            #    maxmiss = 2*max(stat)
            #    miss_target = np.random.uniform(minmiss,maxmiss)
            #    return miss_target
            #if module["type"]=="time":
            #    mintime = min(stat)
            #    maxtime = max(stat)
            #    out = np.random.randint(0.6*mintime,4.0*maxtime,(1,))
            #    return out
            if module["type"] in ["miss_ratios"] + ["time"]:
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
            minmiss = .6*stat.min(axis=1)
            maxmiss = 1*stat.max(axis=1)
            miss_count_target = np.floor(1.5* maxmiss)
            return miss_count_target
        elif module in [f"diff_ratios_bank_{j}" for j in range(self.num_bank)]:
            minmiss = stat.min(axis=1)
            maxmiss = stat.max(axis=1)
            minmiss = (1-np.sign(minmiss)*0.4)*minmiss
            diff_ratios_target = np.random.uniform(minmiss,maxmiss)
            return diff_ratios_target
        elif module=="time_diff":
            mintime = stat.min(axis=1)
            maxtime = stat.max(axis=1)
            times = np.concatenate((np.floor(1.0*np.random.randint(mintime[0],4.0*maxtime[0],(1,))),
                np.floor(1.0*np.random.randint(mintime[1],4.0*maxtime[1],(1,)))))
            return times 
        
