import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History

class GoalGenerator:
    def __init__(self,num_bank):
        self.num_bank = num_bank
        self.k_time = 0
        self.k_miss = 0
    def __call__(self,H:History, module:str)->dict:
        time_module = ["time", "time_diff"]
        miss_modules = [f"miss_bank_{j}" for j in range(self.num_bank)]
        assert module in time_module + miss_modules, f"module {module} unknown"
        stats = H.stats2()
        if module=="time":
            times = np.concatenate((np.floor(.5*np.random.randint(stats["time_core0_alone"]["min"],4.0*stats["time_core0_alone"]["max"],(1,))),
                np.floor(.5*np.random.randint(stats["time_core1_alone"]["min"],4.0*stats["time_core1_alone"]["max"],(1,)))))
            delta = np.random.uniform(.6,4.0,(2,))
            times_together = np.floor(delta*times)
            return np.concatenate((times,times_together))
        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:
            minmiss = np.stack((stats["miss_ratios_core0"]["min"][int(module[-1])],stats["miss_ratios_core1"]["min"][int(module[-1])]))
            minmiss = (1-np.sign(minmiss)*0.4)*minmiss
            maxmiss = 1.5*np.stack((stats["miss_ratios_core0"]["max"][int(module[-1])],stats["miss_ratios_core1"]["max"][int(module[-1])]))
            miss_target = np.random.uniform(minmiss,maxmiss)
            together = np.mean(miss_target*np.random.uniform(.6,4.0,(1,)))
            out = np.zeros(3)
            out[:2] = miss_target
            out[2] = together
            return out

        elif module=="time_diff":
            times = np.concatenate((np.floor(1.0*np.random.randint(stats["diff_time0"]["min"],4.0*stats["diff_time0"]["max"],(1,))),
                np.floor(1.0*np.random.randint(stats["diff_time1"]["min"],4.0*stats["diff_time1"]["max"],(1,)))))
            return times 
        elif module=="ratios_diff":
            minmiss = np.stack((stats["diff_ratios_core0"]["min"],stats["diff_ratios_core0"]["min"]))
            maxmiss = 1.5*np.stack((stats["diff_ratios_core1"]["max"],stats["diff_ratios_core1"]["max"]))
            miss_target = np.random.uniform(minmiss,maxmiss)
            return miss_target
