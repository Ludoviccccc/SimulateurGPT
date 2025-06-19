import numpy as np
import sys
sys.path.append("../../")
from exploration.history import History
from exploration.imgep.goal_generator import GoalGenerator
class IR:
    def __init__(self,modules,
            history:History,
            goal_module:GoalGenerator,
            window:int=10,
            epsilon:float=.1
            ):
        self.epsilon = epsilon
        self.history = history
        self.modules = modules
        self.goal_module = goal_module
        self.diversity = {}
        self.window = window
    def add(self,name:str, div:int) -> None:
        if name in self.diversity:
            self.diversity[name].append(div)
            self.diversity[name] = self.diversity[name][-self.window:]
        else:
            self.diversity[name] = [div]
    def progress(self):
        out = {}
        for key in self.diversity.keys():
            out[key] = np.abs(self.diversity[key][-1] - self.diversity[key][0])/np.abs(self.diversity[key][0])
        return out
    def prob(self)->dict:
        in_ = self.progress()
        sum_ = 0
        probs = {}
        for key in in_.keys():
            sum_ += in_[key]
        for key in in_.keys():
            probs[key] = in_[key]/sum_
        return probs
    def choice(self):
        """
        choose the module to explore, the choice is random, based on the learing progress,
        itself based on the diversity
        """
        probs = self.prob()
        C = np.random.binomial(1,self.epsilon)
        vec = np.zeros(len(self.modules))
        if C:
            vec[np.random.randint(0,len(self.modules))] = 1.0
        probs = (1-C)*np.array(list(probs.values()))+ C*vec
        return self.modules[int(np.random.choice(len(self.modules), 1, p=probs))]
    def __call__(self,
                 parameter:dict[list], 
                 observation:dict[list],
                 goal:np.ndarray):
        for module in self.modules:
            feature = self.goal_module.data2feature(self.history.memory_perf, module)
            #print(feature.shape)
            #print("module", module)
            if type(module) is dict:
                if module["type"] == "miss_ratios":
                    core = module["core"]
                    bank = module["bank"]
                    if core!=None:
                        name = f"miss_core_{core}_bank_{bank}"
                    else:
                        name = f"miss_together_bank_{bank}"
                    bins = np.linspace(0,1,21)
                elif module["type"] == "time":
                    core = module["core"]
                    single = module["single"]
                    if single:
                        name = f"time_{core}_isolation"
                    else:
                        name = f"time_{core}_mutual"
                    bins = np.linspace(0,1000,21)
                elif module["type"] == "miss_ratios_detailled":
                    core = module["core"]
                    bank = module["bank"]
                    row = module["row"]
                    if core!=None:
                        name = f"miss_core_{core}_bank_{bank}_core_{core}"
                    else:
                        name = f"miss_together_bank_{bank}_core_{core}"
                    bins = np.linspace(0,1,21)
                elif module["type"] =="time_diff":
                    bins = np.linspace(0,1000,21)
                    core = module["core"]
                    name = f"time_diff_core{core}"
                hist,_ = np.histogram(feature,bins =bins)
                div = sum(hist>0)
                self.add(name, div=div)
            elif module in [f"miss_bank_{j}" for j in range(self.goal_module.num_bank)]:
                bins = np.linspace(0,1,21)
                hist0,_,_ = np.histogram2d(feature[0,:],feature[2,:], bins=[bins, bins])
                hist1,_,_ = np.histogram2d(feature[1,:],feature[2,:], bins=[bins, bins])
                div = .5*(np.sum(hist0>0)+np.sum(hist1>0))
                self.add(module, div=div)
            elif module in [f"miss_count_bank_{j}" for j in range(self.goal_module.num_bank)]:
                bins = np.linspace(0,1000,21)
                hist,_ = np.histogram(feature,bins =bins)
                div = sum(hist>0)
                self.add(module,div=div)
            elif module in [f"diff_ratios_bank_{j}" for j in range(self.goal_module.num_bank)]:
                bins = np.linspace(0,1,21)
                hist,_,_ = np.histogram2d(feature[0,:],feature[1,:], bins=[bins, bins])
                div = np.sum(hist>0)
                self.add(module,div=div)
            elif module in ["time","time_diff"]:
                bins = np.linspace(0,1000,21)
                hist,_,_ = np.histogram2d(feature[0,:],feature[1,:], bins=[bins, bins])
                div = np.sum(hist>0)
                self.add(module,div=div)

