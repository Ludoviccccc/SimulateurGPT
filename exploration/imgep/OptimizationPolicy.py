import random
import numpy as np

import sys
sys.path.append("../../")
from exploration.imgep.mutation import mutate_paire_instructions, mix_instruction_lists
from exploration.history import History




class OptimizationPolicy:
    def __init__(self,mutation_rate = .1):
        """
        Selects a parameter based on a chosen goal and the history.
        Takes the code corresponding to the closest signature to the desired goal signature
        """
        self.mutation_rate = mutation_rate
    def __call__(self,goal:dict[list],H)->dict:
        closest_code = H.select_closest_code(goal) #most promising sample from the history
        output = self.light_code_mutation(closest_code["program"]) #expansion strategie: small random mutation
        return output
    def light_code_mutation(self,programs):
        mutated0, mutated1 = mutate_paire_instructions(programs["core0"], programs["core1"], mutation_rate = self.mutation_rate)
        return {"core0":[mutated0[:50]],"core1":[mutated1[:50]]}


class OptimizationPolicykNN:
    def __init__(self,k=4, mutation_rate = 0.1,max_len=50):
        self.k = k
        self.mutation_rate = mutation_rate
        self.max_len = max_len
        self.num_bank = 4
    def __call__(self,goal:np.ndarray,H:History, module:str)->dict:
        #assert module in ["time"]+[f"miss_bank_{j}" for j in range(self.num_bank)], f"module {module} is unknown"
        closest_codes = self.select_closest_codes(H,goal, module) #most promising sample from the history
        output = self.mix(closest_codes) #expansion strategie: small random mutation
        return output
    def mix(self,programs):
        mix0, mix1 = mix_instruction_lists(programs["program"]["core0"],self.max_len), mix_instruction_lists(programs["program"]["core1"],self.max_len)
        output = self.light_code_mutation({"core0":mix0[:self.max_len],"core1":mix1[:self.max_len]}) #expansion strategie: small random mutation
        return output 
    def loss(self,goal:np.ndarray, elements:np.ndarray):
        a = goal.reshape(-1,1) 
        return  np.sum((a -elements)**2,axis=0)
    def select_closest_codes(self,H:History,signature: np.ndarray,module:str)->dict:
        assert len(H.memory_program)>0, "history empty"
        if module=="time":
            b,_ = H.times2ndarray()
        elif module in [f"miss_bank_{j}" for j in range(4)]:
            b,_ = H.miss2ndarray(int(module[-1]))
        elif module in [f"miss_count_bank_{j}" for j in range(4)]:
            b,_ = H.miss_count_2ndarray(int(module[-1]))
        elif module=="time_diff":
            b,_ = H.timesdiff2ndarray()
        elif module=="ratios_diff":
            b,_ = H.missdiff2ndarray()
        d = self.loss(signature,b)
        idx = np.argsort(d)[:self.k]
        output = {"program": {"core0":[],"core1":[]},}
        for id_ in idx:
            output["program"]["core0"].append(H.memory_program["core0"][id_])
            output["program"]["core1"].append(H.memory_program["core1"][id_])
        return output
    def light_code_mutation(self,programs:dict[list[dict]]):
        mutated0, mutated1 = mutate_paire_instructions(programs["core0"], programs["core1"],mutation_rate = self.mutation_rate)
        return {"core0":[mutated0[:self.max_len]],"core1":[mutated1[:self.max_len]]}
