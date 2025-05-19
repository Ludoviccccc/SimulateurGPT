import random
import numpy as np

import sys
sys.path.append("../../")
from exploration.imgep.mutation import mutate_paire_instructions, mix_instruction_lists
from exploration.imgep.history import History




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
        mutated0, mutated1 = mutate_paire_instructions(programs["core0"], programs["core1"], self.mutation_rate)
        return {"core0":[mutated0[:50]],"core1":[mutated1[:50]]}


class OptimizationPolicykNN:
    def __init__(self,k=4, mutation_rate = 0.1):
        self.k = k
        self.mutation_rate = .1
    def __call__(self,goal:dict[list],H)->dict:
        closest_codes = self.select_closest_codes(H,goal) #most promising sample from the history
        output = self.mix(closest_codes) #expansion strategie: small random mutation
        return output
    def mix(self,programs):
#        mutated0, mutated1 = mutate_paire_instructions(programs["core0"], programs["core1"])
        mix0, mix1 = mix_instruction_lists(programs["program"]["core0"],50), mix_instruction_lists(programs["program"]["core1"],50)
#        print("mix0", mix0)
        output = self.light_code_mutation({"core0":mix0[:50],"core1":mix1[:50]}) #expansion strategie: small random mutation
        return output 
    def select_closest_codes(self,H:History,signature: dict)->dict:
        assert len(H.memory_program)>0, "history empty"
        b = np.array([h for h in H.memory_signature.values()]).reshape((len(H),-1))
        a = np.array([a for a in signature.values()])
        c = np.abs(a -b)
        #d = np.sum(c**2, axis=1)
        #d = np.sum(c, axis=1)
        d = np.sum(c!=0, axis=1)

        idx = np.argsort(d)[:self.k]

        output = {"program": {"core0":[],
                            "core1":[]},
                }
        for id_ in idx:
            output["program"]["core0"].append(H.memory_program["core0"][id_])
            output["program"]["core1"].append(H.memory_program["core1"][id_])
        return output

    def light_code_mutation(self,programs:dict[list[dict]]):
        #print(programs["core0"])
        #exit()
        mutated0, mutated1 = mutate_paire_instructions(programs["core0"], programs["core1"],self.mutation_rate)
        return {"core0":[mutated0[:50]],"core1":[mutated1[:50]]}
