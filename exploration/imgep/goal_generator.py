import random
import numpy as np
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
