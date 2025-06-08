import numpy as np
import pickle
import os.path
class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = {"core0":[],"core1":[]}
        self.memory_perf = {"miss_ratios":[],
                            "miss_ratios_core0":[],            
                            "miss_ratios_core1":[],            
                            "time_core0_together":[],
                            "time_core1_together":[],
                            "time_core0_alone":[],
                            "time_core1_alone":[],
                            "miss_count":[],
                            "miss_count_core0":[],
                            "miss_count_core1":[],
                                                }
        #self.k=0
    def stats2(self):
        out = {key:{"min":np.min(self.memory_perf[key],axis=0),"max":np.max(self.memory_perf[key],axis=0)} for key in self.memory_perf.keys()}
        return out
    def eviction(self):
        if len(self.memory_program)>self.max_size:
            self.memory_program["core0"] = self.memory_program["core0"][-self.max_size:]
            self.memory_program["core1"] = self.memory_program["core1"][-self.max_size:]
    def purge(self):
        self.memory_program["core0"] = [] 
        self.memory_program["core1"] = []
    def __len__(self):
        return len(self.memory_program["core0"])
    def store(self,sample:dict[list]):
        for j in range(len(sample["program"]["core0"])):
            self.memory_program["core0"].append(sample["program"]["core0"][j])
            self.memory_program["core1"].append(sample["program"]["core1"][j])
        self.memory_perf["miss_ratios"].append(list(sample["perf"]))
        self.memory_perf["miss_ratios_core0"].append(list(sample["perf_core0"]))
        self.memory_perf["miss_ratios_core1"].append(list(sample["perf_core1"]))
        self.memory_perf["time_core0_together"].append(sample["time_core0_together"])
        self.memory_perf["time_core1_together"].append(sample["time_core1_together"])
        self.memory_perf["time_core0_alone"].append(sample["time_core0_alone"])
        self.memory_perf["time_core1_alone"].append(sample["time_core1_alone"])
        self.memory_perf["miss_count"].append(sample["miss_count"])
        self.memory_perf["miss_count_core0"].append(sample["miss_count_core0"])
        self.memory_perf["miss_count_core1"].append(sample["miss_count_core1"])

        self.memory_perf["diff_ratios_core0"] = np.abs(np.array(self.memory_perf["miss_ratios_core0"]) - np.array(self.memory_perf["miss_ratios"]))
        self.memory_perf["diff_ratios_core1"] = np.abs(np.array(self.memory_perf["miss_ratios_core1"]) - np.array(self.memory_perf["miss_ratios"]))
        self.memory_perf["diff_time0"] = np.abs(np.array(self.memory_perf["time_core0_alone"]) - np.array(self.memory_perf["time_core0_together"]))
        self.memory_perf["diff_time1"] = np.abs(np.array(self.memory_perf["time_core1_alone"]) - np.array(self.memory_perf["time_core1_together"]))
        #self.eviction()
    def present_content(self):
        output  = {key:np.array(self.memory_perf[key]) for key in self.memory_perf.keys()}
        return output
    def save_pickle(self, name:str=None):
        k = 0
        name = f"data/{name}_{k}"
        while os.path.isfile(f"data/{name}_{k}"):
            k+=1
            name = f"data/{name}_{k}"
        output  = {key:np.array(self.memory_perf[key]) for key in self.memory_perf.keys()}
        with open(name, "wb") as f:
            pickle.dump(output, f)
    def times2ndarray(self)->(np.ndarray,list[str]):
        keys = ["time_core0_alone", "time_core1_alone","time_core0_together", "time_core1_together"]
        out = np.array([np.array(self.memory_perf[key]) for key in keys])
        return out,keys
    def timesdiff2ndarray(self)->(np.ndarray,list[str]):
        keys = ["time_core0_alone", "time_core1_alone","time_core0_together", "time_core1_together"]
        out = np.array([np.abs(np.array(self.memory_perf[keys[i+2]]) - np.array(self.memory_perf[keys[i]])) for i in range(2)])
        return out,["diff_time0", "diff_time1"]
    def miss2ndarray(self, bank:int):
        keys = ["miss_ratios_core0","miss_ratios_core1","miss_ratios"]
        out = np.array([np.array(self.memory_perf[key])[:,bank] for key in keys])
        return out,keys
    def miss_count_2ndarray(self, bank:int):
        keys = ["miss_count_core0","miss_count_core1","miss_ratios"]
        out = np.array([np.array(self.memory_perf[key])[:,bank] for key in keys])
        return out,keys
    def missdiff2ndarray(self):
        return np.stack((self.memory_perf["diff_time0"],self.memory_perf["diff_time1"]))
