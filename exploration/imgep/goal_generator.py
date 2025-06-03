import random
import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
class GoalGenerator:
    def __init__(self, max_len, num_addr):
        self.num_addr = num_addr
        self.max_len = max_len
    def __call__(self, epsilon = .3)->dict:
        def f():
            len_ = self.max_len
            out = np.ones(self.max_len)*(-1)
            out[:len_] = np.random.randint(0, self.num_addr, (len_,))
            return out
        if np.random.binomial(1,1-epsilon):
            out = np.concatenate((f(),f()))
        else:
            instr = f()
            out = np.concatenate((instr, instr))
        return {"addr":out}

class GoalGenerator2:
    def __init__(self, max_len, num_addr):
        self.num_addr = num_addr
        self.max_len = max_len
        self.k = 0
    def __call__(self,H:History, epsilon = .3,module="time")->dict:
        if module == "time":
            stats = H.stats()
            if self.k%10==0:
                self.mincore0time = stats["time"]["core0"]["min"]
                self.maxcore0time = stats["time"]["core0"]["max"]
                self.mincore1time = stats["time"]["core1"]["min"] 
                self.maxcore1time = stats["time"]["core1"]["max"] 
                self.k==1
            times = np.concatenate((np.floor(.6*np.random.randint(self.mincore0time,self.maxcore0time,(1,))),np.floor(2.0*np.random.randint(self.mincore1time,self.maxcore1time,(1,)))))
            #times_together = np.concatenate((np.floor(.6*np.random.randint(self.mincore0time,self.maxcore0time,(1,))),np.floor(2.0*np.random.randint(self.mincore1time,self.maxcore1time,(1,)))))
            delta = np.random.uniform(1.0,4.0,(2,))
        times_together = np.floor(delta*times)
        return np.concatenate((times,times_together))
