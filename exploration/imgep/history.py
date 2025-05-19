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

    def select_closest_code(self,goal: dict)->dict:
        assert len(self.memory_program)>0, "history empty"
        b = np.array([h for h in self.memory_signature.values()]).reshape((self.k,-1))
        a = np.array([a for a in goal.values()])
        c = np.abs(a -b)
        d = np.sum(c**2, axis=1)
        #d = np.sum(c, axis=1)
#        print("d", d)
#        print("d", d.shape)
        #d = np.sum(c!=0, axis=1)
        idx = np.argmin(d)
        return {"program": {"core0":self.memory_program["core0"][idx],
            "core1": self.memory_program["core1"][idx]},
            "signature": {"addr":self.memory_signature["addr"][idx]}}
    def representation(self, name="image/history_visual"):
        plt.figure()
        plt.scatter(self.memory_signature["core2"],self.memory_signature["core1"])
