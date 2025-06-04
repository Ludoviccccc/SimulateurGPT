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
    def __call__(self,H:History, module="time")->dict:
        stats = H.stats()
        if module == "time":
            if self.k_time%10==0:
                self.mincore0time = stats["time"]["core0"]["min"]
                self.maxcore0time = stats["time"]["core0"]["max"]
                self.mincore1time = stats["time"]["core1"]["min"] 
                self.maxcore1time = stats["time"]["core1"]["max"] 
                self.k_time+=1
            times = np.concatenate((np.floor(.5*np.random.randint(self.mincore0time,self.maxcore0time,(1,))),
                np.floor(4.0*np.random.randint(self.mincore1time,self.maxcore1time,(1,)))))
            delta = np.random.uniform(.6,4.0,(2,))
            times_together = np.floor(delta*times)
            return np.concatenate((times,times_together))
        elif module in [f"miss_bank_{j}" for j in range(self.num_bank)]:
            self.mincore0miss = stats["miss"]["core0"]["min"][int(module[-1])]
            self.mincore1miss = stats["miss"]["core1"]["min"][int(module[-1])]
            self.maxcore0miss = stats["miss"]["core0"]["max"][int(module[-1])]
            self.maxcore1miss = stats["miss"]["core1"]["max"][int(module[-1])]
            self.mintogethermiss = stats["miss"]["together"]["min"][int(module[-1])]
            self.maxtogethermiss = stats["miss"]["together"]["max"][int(module[-1])]
            self.k_miss+=1
            minmiss = np.stack((self.mincore0miss, self.mincore1miss))
            minmiss = (1-np.sign(minmiss)*0.4)*minmiss
            maxmiss = 1.5*np.stack((self.maxcore0miss, self.maxcore1miss))
            miss_target = np.random.uniform(minmiss,maxmiss)
            together = np.mean(miss_target*np.random.uniform(.6,4.0,(1,)))
            out = np.zeros(3)
            out[:2] = miss_target
            out[2] = together
            return out
