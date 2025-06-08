import sys
sys.path.append("../")
from exploration.env.func import Env
from exploration.history import History
from  exploration.imgep.OptimizationPolicy import OptimizationPolicykNN
from exploration.imgep.goal_generator import GoalGenerator
from sim.sim_use import make_random_paire_list_instr
import random

class IMGEP:
    def __init__(self,N:int, N_init:int,E:Env,H:History, G:GoalGenerator, Pi:OptimizationPolicykNN, periode:int = 1, modules = ["time"]+[f"miss_bank_{j}" for j in range(4)]+["time_diff"]+["ratios_diff"]):
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
        self.periode = periode
        self.modules = modules 
    def __call__(self):
        for i in range(self.N):
            if i<self.N_init:
                parameter = make_random_paire_list_instr()
            else:
                #Sample target goal
                if (i-self.N_init)%self.periode==0:
                    module = random.choice(self.modules)
                    goal = self.G(self.H, module = module)
                parameter = self.Pi(goal,self.H, module)
            observation = self.env(parameter)
            self.H.store({"program":parameter}|self.env(parameter))
