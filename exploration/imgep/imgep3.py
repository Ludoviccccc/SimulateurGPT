import sys
sys.path.append("../")
from exploration.env.func import Env
from exploration.history import History
from  exploration.imgep.OptimizationPolicy import OptimizationPolicykNN
from exploration.imgep.goal_generator import GoalGenerator
from sim.sim_use import make_random_paire_list_instr
import random

from exploration.imgep.intrinsic_reward import IR

class IMGEP:
    def __init__(self,
                N:int,
                N_init:int,
                E:Env,
                H:History,
                G:GoalGenerator, 
                Pi:OptimizationPolicykNN,
                ir:IR,
                periode:int = 1,
                modules = ["time"]+[f"miss_bank_{j}" for j in range(4)]+["time_diff"]+["ratios_diff"],
                max_len = 100):
        """
        N: int. The experimental budget
        N_init: int. Number of experiments at random
        H: History. Buffer containing codes and signature pairs
        G: GoalGenerator.
        Pi: OptimizationPolicy.
        """
        self.N = N
        self.env = E
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
        self.ir = ir
        self.periode = periode
        self.modules = modules 
        self.max_len = max_len
        self.start = 0


        self.periode_expl = 5
    def take(self,sample:dict,N_init:int): 
        print("sampl", sample.keys())
        for key in sample["memory_perf"].keys():
            self.H.memory_perf[key]= list(sample["memory_perf"][key][:N_init])
        self.H.memory_program["core0"] = sample["memory_program"]["core0"][:N_init]
        self.H.memory_program["core1"] = sample["memory_program"]["core1"][:N_init]
        self.start = N_init
    def __call__(self,lp=True):
        for i in range(self.start,self.N):
            if i<self.N_init:
                parameter = make_random_paire_list_instr(self.max_len,num_addr=self.env.num_addr)
            else:
                #Sample target goal
                if (i-self.N_init)%self.periode==0 and i>=self.N_init:
                    if lp:
                        if self.k%self.periode_expl==0:
                            self.time_explor = i + 100
                        if i<self.time_explor or len(self.ir.diversity)!=len(self.modules) or len(list(self.ir.diversity.values())[0])<3:
                            self.ir(parameter=parameter,
                                    observation=observation,
                                    goal=goal)
                            module = random.choice(self.modules)
                        else:
                            module = self.ir.choice()
                            self.k+=1
                    else:
                            module = self.ir.choice()
                    goal = self.G(self.H, module = module)
                parameter = self.Pi(goal,self.H, module)
            observation = self.env(parameter)
            self.H.store({"program":parameter}|observation)
