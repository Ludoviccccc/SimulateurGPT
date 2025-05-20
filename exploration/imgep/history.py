import numpy as np
class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = {"core0":[],
                                "core1":[]}
        self.memory_signature = {"addr":[]}
        self.k=0
    def store(self,sample:dict[list]):
        for j in range(len(sample["program"]["core0"])):
            self.memory_program["core0"].append(sample["program"]["core0"][j])
            self.memory_program["core1"].append(sample["program"]["core1"][j])
            self.memory_signature["addr"].append(sample["addr"][j])
        self.eviction()
    def eviction(self):
        if len(self.memory_program)>self.max_size:
            self.memory_program["core0"] = self.memory_program["core0"][-self.max_size:]
            self.memory_program["core1"] = self.memory_program["core1"][-self.max_size:]
            self.memory_signature["addr"] = self.memory_signature["addr"][-self.max_size:]
    def purge(self):
        self.memory_program["core0"] = [] 
        self.memory_program["core1"] = []
        self.memory_signature["addr"] = []
    def __len__(self):
        return len(self.memory_program["core0"])

    def representation(self, name="image/history_visual"):
        plt.figure()
        plt.scatter(self.memory_signature["core2"],self.memory_signature["core1"])
