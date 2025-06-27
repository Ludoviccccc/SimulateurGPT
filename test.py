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
from visu import diversity_time_iteration2
from visu2 import comparaison3, comparaison_ratios_iterations, comparaison_ratios_global_iterations
from exploration.imgep.intrinsic_reward import IR
def test(num_bank):
    N = 500
    N_init = 50
    mutation_rate  = .1
    periode = 10
    num_addr = 20
    modules = [{"type":"miss_ratios_detailled","bank":bank,"core":core,"row":row} for core in [None,0,1] for bank in range(num_bank) for row in range(num_addr//16)]
    modules += [{"type":"time_diff","core":core} for core in range(2)]
    modules += ["time"]
    for k in [1]:
        print(f"start: k = {k}, N={N}")
        G = GoalGenerator(num_bank = num_bank, modules = modules)
        Pi = OptimizationPolicykNN(k=k,mutation_rate=mutation_rate,max_len=max_len)
        H_imgep = History(max_size=N)
        ir = IR(modules,H_imgep, G, window = periode)
        imgep = IMGEP(N,N_init, En,H_imgep,G,Pi,ir, periode = periode, modules = modules)
        imgep()
        H_imgep.save_pickle(f"history_kNN_{k}_N_{N}_test")
        print(f"done")
if __name__=="__main__":
    #np.random.seed(0)
    folder = "data3"
    folder1module = "data_1module"
    image_folder ="image3"
    test_mode = False
    num_addr = 20
    N = int(10000)
    N_init = 1000
    max_len = 50
    periode = 15
    num_bank = 4 # m'est pas variable, a changer dans dossier simulation
    mutation_rate = .1
    #modules =   ["time"]
    modules =  [f"miss_bank_{j}" for j in range(num_bank)]
    modules +=  [f"diff_ratios_bank_{j}" for j in range(num_bank)]
    #modules +=  [{"type":"time_diff","core":core} for core in range(2)]
    modules +=  [{"type":"miss_count", "bank":bank} for bank in range(num_bank)]
    modules += [{"type":"miss_ratios_global"}]
    modules += [{"type":"miss_ratios_global_time"}]
    dict_modules = [{"type":"miss_ratios","bank":bank, "core":core} for core in [None, 0,1] for bank in range(num_bank)]
    #dict_modules2 = [{"type":"time", "core":core,"single":single} for core in range(2) for single in [True, False]]

    ratios_detailled = [{"type":"miss_ratios_detailled","bank":bank,"core":core,"row":row} for core in [None,0,1] for bank in range(num_bank) for row in range(num_addr//16)]
    modules = modules + dict_modules + ratios_detailled
    #modules +=dict_modules2 
    #modules = [{"type":"miss_ratios_global_time"}]
    print("nomb modules", len(modules))
    En = Env(repetition=1)

    H_rand = History(max_size= N)
    H2_rand = History(max_size=N)
    rand = RANDOM(N = N,E = En, H = H_rand, H2 = H2_rand,max_=max_len)

    if test_mode:
        test(num_bank)
        exit()

    try:
        with open(f"{folder1module}/history_rand_N_{N}_{0}", "rb") as f:
            sample_rand = pickle.load(f)
            content_random = sample_rand["memory_perf"]
    except:
        print("start random exploration")
        rand()
        print("done")
        #save results
        H_rand.save_pickle(f"{folder1module}/history_rand_N_{N}")
        with open(f"{folder1module}/history_rand_N_{N}_{0}", "rb") as f:
            sample_rand = pickle.load(f)
            content_random = sample_rand["memory_perf"]
    ks = [1,2,3,4]
    for lp in [True,False]:
        for k in ks:
            print(f"start: k = {k}, N={N}")
            G = GoalGenerator(num_bank = num_bank, modules = modules)
            Pi = OptimizationPolicykNN(k=k,mutation_rate=mutation_rate,max_len=max_len)
            H_imgep = History(max_size=N)
            ir = IR(modules,H_imgep, G, window = periode)
            imgep = IMGEP(N,N_init, En,H_imgep,G,Pi,ir, periode = periode, modules = modules, max_len = max_len)
            imgep.take(sample_rand,N_init)
            imgep(lp=lp)
            if lp:
                H_imgep.save_pickle(f"{folder}/history_kNN_{k}_N_{N}_lp")
            else:
                H_imgep.save_pickle(f"{folder}/history_kNN_{k}_N_{N}_no_lp")
            print(f"done")
    N = 10000
    ks = []
    lp = True
    if lp:
        file = lambda k,N: f"{folder}/history_kNN_{k}_N_{N}_lp_0" 
    else:
        file = lambda k,N: f"{folder}/history_kNN_{k}_N_{N}_no_lp_0"
    for k_moins_un,name in [(k,file(k,N)) for k in ks]:
        with open(name, "rb") as f:
            sample = pickle.load(f)
            content_imgep = sample["memory_perf"]
        file_names = [f"{image_folder}/comp_ratios_{k_moins_un}_{N}",f"{image_folder}/comp_times_k{k_moins_un}_{N}",f"{image_folder}/comp_count_{k_moins_un}_{N}"]
        if lp:
            file_names = [f+"_lp" for f in file_names]
        else:
            file_names = [f+"_no_lp" for f in file_names]
        comparaison3(content_random, content_imgep, name = file_names)
    ks = [1,2,3,4]
    #exit()
    for k in ks:
        diversity_time_iteration2(content_random,
                                [("imgep no lp",k,f"{folder}/history_kNN_{k}_N_{N}_no_lp_0")]
                                +[("imgep -lp",k,f"{folder}/history_kNN_{k}_N_{N}_lp_0")],
                                #+ [("imgep 1 module",k,f"{folder1module}/history_kNN_{k}_N_{N}_no_lp_0")],
                                title = f"comparaison_time_diversity_{k}",
                                folder = image_folder)



    for k in [1,2,3,4]:
        with open(f"{folder}/history_kNN_{k}_N_{N}_no_lp_0", "rb") as f:
            sample = pickle.load(f)
            content_imgep_no_lp = sample["memory_perf"] 
        with open(f"{folder}/history_kNN_{k}_N_{N}_lp_0", "rb") as f:
            sample = pickle.load(f)
            content_imgep_lp = sample["memory_perf"]
        #with open(f"{folder1module}/history_kNN_{k}_N_{N}_no_lp_0", "rb") as f:
        #    sample = pickle.load(f)
        #    content_imgep_no_lp_1module = sample["memory_perf"] 
        #with open(f"data_1module/history_kNN_{k}_N_{N}_lp_0", "rb") as f:
        #    sample = pickle.load(f)
        #    content_imgep_lp = sample["memory_perf"]
        comparaison_ratios_iterations(("random",content_random),
                                     ("imgep -lp",content_imgep_lp),
                                     ("imgep - no lp",content_imgep_no_lp),
                                     #("imgep - no lp 1 module",content_imgep_no_lp_1module),
                                     name = f"{image_folder}/comp_ratios_iteration_{k}_{N}_lp_vs_no_lp", k = k)
        comparaison_ratios_global_iterations(("random",content_random),
                                            ("imgep -lp",content_imgep_lp),
                                            ("imgep - no lp",content_imgep_no_lp),
                                           # ("imgep - no lp 1 module",content_imgep_no_lp_1module),
                                            name = f"{image_folder}/comp_global_ratios_iteration_{k}_{N}_lp_vs_no_lp", k = k)
