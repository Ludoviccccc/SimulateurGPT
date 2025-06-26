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
                parameter = make_random_paire_list_instr(self.max_len)
            else:
                #Sample target goal
                if (i-self.N_init)%self.periode==0 and i>=self.N_init:
                    if lp and len(self.ir.diversity)==len(self.modules) and len(list(self.ir.diversity.values())[0])>=3:
                        module = self.ir.choice()
                    else:
                        module = random.choice(self.modules)
                    goal = self.G(self.H, module = module)
                parameter = self.Pi(goal,self.H, module)
            observation = self.env(parameter)
            if (i-self.N_init)%self.periode==0 and i>=self.N_init and lp:
                self.ir(parameter=parameter,
                        observation=observation,
                        goal=goal)
                #if len(self.ir.diversity)==len(self.modules) and len(list(self.ir.diversity.values())[0])>=2:
                #    progress = self.ir.progress()
            self.H.store({"program":parameter}|observation)
