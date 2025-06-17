import random
import numpy as np

import sys
sys.path.append("../../")
from exploration.imgep.mutation import mutate_paire_instructions, mix_instruction_lists
from exploration.history import History
from exploration.imgep.features import Features




class OptimizationPolicykNN(Features):
    def __init__(self,
                k=4,
                mutation_rate = 0.1,
                max_len=50):
        super().__init__()
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
        if type(goal)!=float:
            a = goal.reshape(-1,1) 
        else:
            a = np.array([goal]).reshape(-1,1) 
        return  np.sum((a -elements)**2,axis=0)
    def select_closest_codes(self,H:History,signature: np.ndarray,module:str)->dict:
        t = False
        assert len(H.memory_program)>0, "history empty"
        if module=="time":
            keys = ["time_core0_alone", "time_core1_alone","time_core0_together", "time_core1_together"]
            b = np.array([np.array(H.memory_perf[key]) for key in keys])
        elif module in [f"miss_bank_{j}" for j in range(4)]:
            keys = ["miss_ratios_core0","miss_ratios_core1","miss_ratios"]
            bank = int(module[-1])
            b = np.array([np.array(H.memory_perf[key])[:,bank] for key in keys])
        elif module in [f"miss_count_bank_{j}" for j in range(4)]:
            keys = ["miss_count_core0","miss_count_core1","miss_ratios"]
            bank = int(module[-1])
            b = np.array([np.array(H.memory_perf[key])[:,bank] for key in keys])
        elif module=="time_diff":
            keys = ["time_core0_alone", "time_core1_alone","time_core0_together", "time_core1_together"]
            b = np.array([np.abs(np.array(H.memory_perf[keys[i+2]]) - np.array(H.memory_perf[keys[i]])) for i in range(2)])
        elif module in [f"diff_ratios_bank_{j}" for j in range(4)]:
            bank = int(module[-1])
            keys = [f"diff_ratios_core{j}" for j in range(2)]
            b = np.array([np.array(H.memory_perf[key])[:,bank] for key in keys])
        elif type(module)==dict:
            t = True
            if module["type"]=="miss_ratios":
                #bank = module["bank"]
                #core = module["core"]
                #if core:
                #    keys = [f"miss_ratios_core{core}"]
                #else:
                #    keys = ["miss_ratios"]
                #b = np.array([np.array(H.memory_perf[key])[:,bank] for key in keys])
                b = self.data2feature(H.memory_perf,module)
            if module["type"]=="miss_ratios_detailled":
                #bank = module["bank"]
                #core = module["core"]
                #row = module["row"]
                #if core:
                #    keys = [f"miss_ratios_core{core}"]
                #else:
                #    keys = ["miss_ratios"]
                #b = np.array([np.array(H.memory_perf[key])[:,row,bank] for key in keys])
                b = self.data2feature(H.memory_perf, module)
            elif module["type"]=="time":
                core = module["core"]
                single = module["single"]
                if single:
                    keys = [f"time_core{core}_alone"]
                else:
                    keys = [f"time_core{core}_together"]
                b = np.array([np.array(H.memory_perf[key]) for key in keys])
        ##########################################
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
