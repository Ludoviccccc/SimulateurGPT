from sim.class_mem_sim import Interconnect, MultiLevelCache
from sim.ddr import DDRMemory
import random
import time
import numpy as np
from sim.sim_use import runpgrms, make_random_list_instr, make_random_paire_list_instr
from exploration.random.func import RANDOM, Env
#from exploration.imgep.history import History, History
from exploration.history import History
from exploration.imgep.goal_generator import GoalGenerator
from exploration.imgep.OptimizationPolicy import OptimizationPolicy, OptimizationPolicykNN
from exploration.imgep.mutation import mutate_paire_instructions 
import matplotlib.pyplot as plt


if __name__=="__main__":
#    random.seed(0)
    N = int(100)
    max_len = 500  
    length_programs = 100


    H = History(max_size=1000)
    En = Env(length_programs=length_programs, max_len=max_len)
    imgep = RANDOM(N = N,E = En, H = H)
    imgep()
    print(H.present_content())
