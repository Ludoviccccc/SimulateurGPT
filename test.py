import random
import time
import numpy as np
from exploration.random.func import RANDOM
from exploration.env.func import Env
from exploration.history import History
from exploration.imgep.goal_generator import GoalGenerator
from exploration.imgep.OptimizationPolicy import OptimizationPolicykNN
from exploration.imgep.imgep import IMGEP
import matplotlib.pyplot as plt
from visu import representation, comparaison

if __name__=="__main__":
    #random.seed(0)
    N = int(2000)
    N_init = 500
    max_len = 1000  
    length_programs = 100
    k = 4
    periode = 20
    num_bank = 4

    H_rand = History(max_size=2000)
    H2_rand = History(max_size=2000)
    En = Env(length_programs=length_programs, max_len=max_len)
    rand = RANDOM(N = N,E = En, H = H_rand, H2 = H2_rand)
    rand()
    content_random = H_rand.present_content()
    modules = ["time"]+ ["time_diff"]+[f"miss_bank_{j}" for j in range(4)]+["ratios_diff"]+ [f"miss_count_bank_{j}" for j in range(num_bank)]
    for k in [2]:
        G = GoalGenerator(num_bank = num_bank)
        Pi = OptimizationPolicykNN(k=k,mutation_rate=.1,max_len=50)
        H_imgep = History(max_size=1000)
        H2_imgep = History(max_size=1000)
        imgep = IMGEP(N,N_init, En,H_imgep,G,Pi, periode = periode, modules = modules)
        imgep()
        content_imgep = H_imgep.present_content()
        comparaison(content_random, content_imgep, name = [f"image/comp_ratios_{k}",f"image/comp_times_k{k}"])
        print(f"done: k = {k}")
