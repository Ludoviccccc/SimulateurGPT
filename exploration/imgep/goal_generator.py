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
    def __call__(self,H:History, module:str)->dict:
        assert module in self.modules, f"module {module} unknown"
        stats = H.stats2()

        if module=="time":
            times = np.concatenate((np.floor(np.random.randint(0.6*stats["time_core0_alone"]["min"],4.0*stats["time_core0_alone"]["max"],(1,))),
                np.floor(np.random.randint(.5*stats["time_core1_alone"]["min"],4.0*stats["time_core1_alone"]["max"],(1,)))))
            delta = np.random.uniform(.6,4.0,(2,))
            times_together = np.floor(delta*times)
            return np.concatenate((times,times_together))


        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:
            minmiss = np.stack((stats["miss_ratios_core0"]["min"][int(module[-1])],
                                stats["miss_ratios_core1"]["min"][int(module[-1])],
                                stats["miss_ratios"]["min"][int(module[-1])]))
            #minmiss = .1+(1-np.sign(minmiss)*0.4)*minmiss
            maxmiss = 2*np.stack((stats["miss_ratios_core0"]["max"][int(module[-1])],
                                  stats["miss_ratios_core1"]["max"][int(module[-1])],
                                  stats["miss_ratios"]["max"][int(module[-1])])
                                   )
            miss_target = np.random.uniform(minmiss,maxmiss)
            miss_target = 1.5*maxmiss
            return miss_target
        elif type(module)==dict: 
            if module["type"]=="miss_ratios":
                bank = module["bank"]
                core = module["core"]
                if core:
                    minmiss = stats[f"miss_ratios_core{core}"]["min"][bank]
                    minmiss = (1-np.sign(minmiss)*0.4)*minmiss
                    maxmiss = 2*stats[f"miss_ratios_core{core}"]["max"][bank]

                else:
                    minmiss = stats["miss_ratios"]["min"][bank] 
                    maxmiss = 2*stats["miss_ratios"]["max"][bank]
                miss_target = np.random.uniform(minmiss,maxmiss)
                return miss_target
            if module["type"]=="time":
                core = module["core"]
                single = module["single"]
                if single:
                    out = np.random.randint(0.6*stats[f"time_core{core}_alone"]["min"],4.0*stats[f"time_core{core}_alone"]["max"],(1,))
                else:
                    out = np.random.randint(0.6*stats[f"time_core{core}_together"]["min"],4.0*stats[f"time_core{core}_together"]["max"],(1,))
                return out
        elif module in [f"miss_count_bank_{j}" for j in range(self.num_bank)]:
            minmiss = np.stack((stats["miss_count_core0"]["min"][int(module[-1])],
                                stats["miss_count_core1"]["min"][int(module[-1])],
                                stats["miss_count"]["min"][int(module[-1])]))
            minmiss = (1-np.sign(minmiss)*0.4)*minmiss
            maxmiss = np.stack((stats["miss_count_core0"]["max"][int(module[-1])],
                                  stats["miss_count_core1"]["max"][int(module[-1])],
                                  stats["miss_count"]["max"][int(module[-1])])
                                   )
            miss_count_target = 1.5* maxmiss
            return miss_count_target
        elif module in [f"diff_ratios_bank_{j}" for j in range(self.num_bank)]:
            minmiss = np.stack((stats["diff_ratios_core0"]["min"][int(module[-1])],
                                stats["diff_ratios_core1"]["min"][int(module[-1])]
                                ))
            minmiss = (1-np.sign(minmiss)*0.4)*minmiss
            maxmiss = np.stack((stats["diff_ratios_core0"]["max"][int(module[-1])],
                                  stats["diff_ratios_core1"]["max"][int(module[-1])]))
            diff_ratios_target = np.random.uniform(minmiss,maxmiss)
            return diff_ratios_target

        elif module=="time_diff":
            times = np.concatenate((np.floor(1.0*np.random.randint(stats["diff_time0"]["min"],4.0*stats["diff_time0"]["max"],(1,))),
                np.floor(1.0*np.random.randint(stats["diff_time1"]["min"],4.0*stats["diff_time1"]["max"],(1,)))))
            return times 
        elif module=="ratios_diff":
            minmiss = np.stack((stats["diff_ratios_core0"]["min"],stats["diff_ratios_core0"]["min"]))
            maxmiss = 1.0*np.stack((stats["diff_ratios_core1"]["max"],stats["diff_ratios_core1"]["max"]))
            miss_target = np.random.uniform(minmiss,maxmiss)
            return miss_target
