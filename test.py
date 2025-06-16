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
from visu import representation, comparaison, comparaison_ratios_iterations, diversity_time_iteration, diversity_time_iteration2
from exploration.imgep.intrinsic_reward import IR
def test(modules,num_bank):
    N = 500
    N_init = 50
    mutation_rate  = .1
    periode = 10
    for k in [1]:
        print(f"start: k = {k}, N={N}")
        G = GoalGenerator(num_bank = num_bank, modules = modules)
        Pi = OptimizationPolicykNN(k=k,mutation_rate=mutation_rate,max_len=max_len)
        H_imgep = History(max_size=N)
        ir = IR(modules,H_imgep, G)
        imgep = IMGEP(N,N_init, En,H_imgep,G,Pi,ir, periode = periode, modules = modules)
        imgep()
        H_imgep.save_pickle(f"history_kNN_{k}_N_{N}")
        print(f"done")
if __name__=="__main__":
    np.random.seed(0)
    test_mode = False
    N = int(2000)
    N_init = 500
    max_len = 50
    k = 4
    periode = 20
    num_bank = 4 # m'est pas variable, a changer dans dossier simulation
    mutation_rate = .1
    modules = ["time"]+ ["time_diff"]+[f"miss_bank_{j}" for j in range(num_bank)]+[f"miss_count_bank_{j}" for j in range(num_bank)]+[f"diff_ratios_bank_{j}" for j in range(num_bank)]
    dict_modules = [{"type":"miss_ratios","bank":bank, "core":core} for core in [None, 0,1] for bank in range(num_bank)]
    dict_modules2 = [{"type":"time", "core":core,"single":single} for core in range(2) for single in [True, False]]
    modules = modules + dict_modules2 + dict_modules
    En = Env()

    H_rand = History(max_size= N)
    H2_rand = History(max_size=N)
    rand = RANDOM(N = N,E = En, H = H_rand, H2 = H2_rand,max_=max_len)

    if test_mode:
        test(modules, num_bank)

    try:
        with open(f"data/history_rand_N_{N}_{0}", "rb") as f:
            content_random = pickle.load(f)
    except:
        rand()
        #save results
        H_rand.save_pickle(f"history_rand_N_{N}")
        with open(f"data/history_rand_N_{N}_{0}", "rb") as f:
            content_random = pickle.load(f)
    ks = []
    for k in ks:
        print(f"start: k = {k}, N={N}")
        G = GoalGenerator(num_bank = num_bank, modules = modules)
        Pi = OptimizationPolicykNN(k=k,mutation_rate=mutation_rate,max_len=max_len)
        H_imgep = History(max_size=N)
        ir = IR(modules,H_imgep, G)
        imgep = IMGEP(N,N_init, En,H_imgep,G,Pi,ir, periode = periode, modules = modules)
        imgep()
        H_imgep.save_pickle(f"history_kNN_{k}_N_{N}")
        print(f"done")
    N = 2000
    ks = [1,2,3,4]
    
    for k_moins_un,name in [(k,f"data/history_kNN_{k}_N_{N}_0") for k in ks]:
        with open(name, "rb") as f:
            content_imgep = pickle.load(f)
        comparaison(content_random, content_imgep, name = [f"image/comp_ratios_{k_moins_un}",f"image/comp_times_k{k_moins_un}",f"image/comp_count_{k_moins_un}"])
        comparaison_ratios_iterations(content_random, content_imgep, name = f"comp_ratios_iteration_{k_moins_un}", k = k_moins_un + 1)
        diversity_time_iteration(content_random, content_imgep, f"time_diversity_{k_moins_un}",title=f"time, k = {k_moins_un}")
    ks = [1,2,3,4,5]
    diversity_time_iteration2(content_random,[(k,f"data/history_kNN_{k}_N_{N}_0") for k in ks],"comparaison_time_diversity")