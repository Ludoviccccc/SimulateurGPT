import random
import pickle
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
    #N = 10
    #N_init = 3
    max_len = 1000  
    length_programs = 100
    k = 4
    periode = 20
    num_bank = 4 # n'est pas variable, a changer dans la classe Env
    mutation_rate = .1

    H_rand = History(max_size= N)
    H2_rand = History(max_size=N)

    En = Env(length_programs=length_programs, max_len=max_len)
    rand = RANDOM(N = N,E = En, H = H_rand, H2 = H2_rand)
    if False:
        rand()
        #save results
        H_rand.save_pickle(f"history_rand_N_{N}")
    with open(f"data/history_rand_N_{N}_{0}", "rb") as f:
        content_random = pickle.load(f)
    modules = ["time"]+ ["time_diff"]+[f"miss_bank_{j}" for j in range(num_bank)]+["ratios_diff"]+ [f"miss_count_bank_{j}" for j in range(num_bank)]
    for k in []:
        print(f"start: k = {k}")
        G = GoalGenerator(num_bank = num_bank)
        Pi = OptimizationPolicykNN(k=k,mutation_rate=mutation_rate,max_len=50)
        H_imgep = History(max_size=N)
        imgep = IMGEP(N,N_init, En,H_imgep,G,Pi, periode = periode, modules = modules)
        imgep()
        H_imgep.save_pickle(f"history_kNN_{k}_N_{N}")
        print(f"done: k = {k}")
    N = 2000
    for k_moins_un,name in enumerate([f"data/history_kNN_{k}_N_{N}_0" for k in range(1,4)]):
        with open(name, "rb") as f:
            content_imgep = pickle.load(f)
        comparaison(content_random, content_imgep, name = [f"image/comp_ratios_{k_moins_un +1}",f"image/comp_times_k{k_moins_un+1}"])
