import numpy as np
class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = {"core0":[],"core1":[]}
        keys = ["addr", "bank","bank0", "bank1", "bank2", "bank3", "delay", "status", "completion_time", "time", "max_radius", "pending_addr", "pending_core_id"]
        self.cat = ["core0","core1", "core0_alone", "core1_alone"]
        self.memory_signature = {key : {kkey :[] for kkey in keys} for key in self.cat}
        self.k=0
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
    def store(self,sample:dict[list]):
        for j in range(len(sample["program"]["core0"])):
            self.memory_program["core0"].append(sample["program"]["core0"][j])
            self.memory_program["core1"].append(sample["program"]["core1"][j])
        for c in self.cat:
            for key in self.memory_signature[c].keys():
                self.memory_signature[c][key].append(sample[c][key])
        self.eviction()
