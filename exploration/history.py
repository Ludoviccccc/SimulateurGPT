import numpy as np
class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = {"core0":[],"core1":[]}
        keys = ["addr", "bank","bank0", "bank1", "bank2", "bank3", "delay", "status", "completion_time", "time", "max_radius", "pending_addr", "pending_core_id"]
        self.cat = ["core0","core1", "core0_alone", "core1_alone"]
        self.memory_perf = {"miss_ratios":[],
                            "miss_ratios_core0":[],            
                            "miss_ratios_core1":[],            
                            "time_core0_together":[],
                            "time_core1_together":[],
                            "time_core0_alone":[],
                            "time_core1_alone":[],
                                                }
        self.memory_signature = {key : {kkey :[] for kkey in keys} for key in self.cat}
        self.k=0
    def stats(self):
        maxcore0 = max(self.memory_perf["time_core0_alone"])
        mincore0 = min(self.memory_perf["time_core0_alone"])
        maxcore1 = max(self.memory_perf["time_core1_alone"])
        mincore1 = min(self.memory_perf["time_core1_alone"])
        mintogeth = np.min(self.memory_perf["miss_ratios"],axis=0)
        maxtogeth = np.max(self.memory_perf["miss_ratios"],axis=0)
        minmiss0 = np.min(self.memory_perf["miss_ratios_core0"],axis=0)
        maxmiss0 = np.max(self.memory_perf["miss_ratios_core0"],axis=0)
        minmiss1 = np.min(self.memory_perf["miss_ratios_core1"],axis=0)
        maxmiss1 = np.max(self.memory_perf["miss_ratios_core1"],axis=0)
        return {"time":{"core0":{"min":mincore0, "max":maxcore0},
                       "core1":{"min":mincore1, "max":maxcore1}},
                       "miss": {"together":{"min":mintogeth,"max":maxtogeth},
                         "core0":{"min":minmiss0, "max":maxmiss0},
                         "core1":{"min":minmiss1, "max":maxmiss1}}}
    def eviction(self):
        if len(self.memory_program)>self.max_size:
            self.memory_program["core0"] = self.memory_program["core0"][-self.max_size:]
            self.memory_program["core1"] = self.memory_program["core1"][-self.max_size:]
        for c in self.cat:
            for key in self.memory_signature[c].keys():
                self.memory_signature[c][key] = self.memory_signature[c][key][-self.max_size:]
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
        self.memory_perf["miss_ratios"].append(list(sample["perf"]))
        self.memory_perf["miss_ratios_core0"].append(list(sample["perf_core0"]))
        self.memory_perf["miss_ratios_core1"].append(list(sample["perf_core1"]))
        self.memory_perf["time_core0_together"].append(sample["time_core0_together"])
        self.memory_perf["time_core1_together"].append(sample["time_core1_together"])
        self.memory_perf["time_core0_alone"].append(sample["time_core0_alone"])
        self.memory_perf["time_core1_alone"].append(sample["time_core1_alone"])
        self.eviction()
    def present_content(self):
        output  = {key:np.array(self.memory_perf[key]) for key in self.memory_perf.keys()}
        return output
    def times2ndarray(self)->(np.ndarray,list[str]):
        keys = ["time_core0_alone", "time_core1_alone","time_core0_together", "time_core1_together"]
        out = np.array([np.array(self.memory_perf[key]) for key in keys])
        return out,keys
    def miss2ndarray(self, bank:int):
        keys = ["miss_ratios_core0","miss_ratios_core1","miss_ratios"]
        out = np.array([np.array(self.memory_perf[key])[:,bank] for key in keys])
        return out,keys
