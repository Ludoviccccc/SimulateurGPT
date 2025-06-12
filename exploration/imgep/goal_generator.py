import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History

class GoalGenerator:
    def __init__(self,num_bank:int,modules:list):
        self.num_bank = num_bank
        self.k_time = 0
        self.k_miss = 0
        self.modules = modules
    def data2feature(self,stats:dict,module:str)->np.ndarray:
        if module=="time":
            out = np.stack((stats["time_core0_alone"],stats["time_core1_alone"]))
        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:
            out = np.stack((np.array(stats["miss_ratios_core0"])[:,int(module[-1])],
                            np.array(stats["miss_ratios_core1"])[:,int(module[-1])],
                            np.array(stats["miss_ratios"])[:,int(module[-1])]))
        elif type(module)==dict: 
            if module["type"]=="miss_ratios":
                bank = module["bank"]
                core = module["core"]
                if core:
                    out = np.array(stats[f"miss_ratios_core{core}"])[:,bank]
                else:
                    out = np.array(stats[f"miss_ratios"])[:,bank]
            if module["type"]=="time":
                core = module["core"]
                single = module["single"]
                if single:
                    out = stats[f"time_core{core}_alone"]
                else:
                    out = stats[f"time_core{core}_together"]
                return out
        elif module in [f"miss_count_bank_{j}" for j in range(self.num_bank)]:
            out  = np.stack((np.array(stats["miss_count_core0"])[:,int(module[-1])],
                np.array(stats["miss_count_core1"])[:,int(module[-1])],
                np.array(stats["miss_count"])[:,int(module[-1])]))
        elif module in [f"diff_ratios_bank_{j}" for j in range(self.num_bank)]:
            out = np.stack((np.array(stats["diff_ratios_core0"])[:,int(module[-1])],
                np.array(stats["diff_ratios_core1"])[:,int(module[-1])]))
        elif module=="time_diff":
            out = np.stack((np.array(stats["diff_time0"]),np.array(stats["diff_time1"])))
        return out
    def __call__(self,H:History, module:str)->np.ndarray:
        assert module in self.modules, f"module {module} unknown"
        #stats = H.stats2()
        stats_ = H.memory_perf
        if module=="time":
            stat = self.data2feature(stats_, module)
            times = np.random.randint(.6*stat.min(axis=1), 4*stat.max(axis=1))
            delta = np.random.uniform(.6,4.0,(2,))
            times_together = np.floor(delta*times)
            return np.concatenate((times,times_together))


        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:

            stat = self.data2feature(stats_, module)
            minmiss = .6*stat.min(axis=1)
            maxmiss = 1*stat.max(axis=1)
            miss_target = np.random.uniform(minmiss,maxmiss)
            miss_target = 1.5*maxmiss
            return miss_target
        elif type(module)==dict: 
            if module["type"]=="miss_ratios":
                bank = module["bank"]
                core = module["core"]
                stat = self.data2feature(stats_, module)
                minmiss = min(stat)
                maxmiss = 2*max(stat)
                miss_target = np.random.uniform(minmiss,maxmiss)
                return miss_target
            if module["type"]=="time":
                stat = self.data2feature(stats_, module)
                mintime = min(stat)
                maxtime = max(stat)
                core = module["core"]
                single = module["single"]
                out = np.random.randint(0.6*mintime,4.0*maxtime,(1,))
                return out
        elif module in [f"miss_count_bank_{j}" for j in range(self.num_bank)]:
            stat = self.data2feature(stats_, module)
            minmiss = .6*stat.min(axis=1)
            maxmiss = 1*stat.max(axis=1)
            miss_count_target = 1.5* maxmiss
            return miss_count_target
        elif module in [f"diff_ratios_bank_{j}" for j in range(self.num_bank)]:
            stat = self.data2feature(stats_, module)
            minmiss = stat.min(axis=1)
            maxmiss = stat.max(axis=1)
            minmiss = (1-np.sign(minmiss)*0.4)*minmiss
            diff_ratios_target = np.random.uniform(minmiss,maxmiss)
            return diff_ratios_target

        elif module=="time_diff":
            stat = self.data2feature(stats_, module)
            mintime = stat.min(axis=1)
            maxtime = stat.max(axis=1)
            times = np.concatenate((np.floor(1.0*np.random.randint(mintime[0],4.0*maxtime[0],(1,))),
                np.floor(1.0*np.random.randint(mintime[1],4.0*maxtime[1],(1,)))))
            return times 
