
import pickle
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
import json
import sys
if __name__=="__main__":
    #np.random.seed(0)
    folder1module = "data_1module"
    with open(sys.argv[1],"rb") as f:
        config = json.load(f)
    modules = config["modules"]
    periode = config["periode"]
    mutation_rate = config["mutation_rate"]
    N = config["N"]
    N_init = config["N_init"]
    num_bank = config["num_bank"]
    max_len = config["max_len"]
    folder = config["folder"]
    num_addr = config["num_addr"]
    image_folder = config["image_folder"]
    ks_ = config["ks"]
    print("nomb modules", len(modules))
    En = Env(repetition=1)

    H_rand = History(max_size= N)
    H2_rand = History(max_size=N)
    rand = RANDOM(N = N,E = En, H = H_rand, H2 = H2_rand,max_=max_len)

    with open(f"{folder}/history_rand_N_{N}_{0}.pkl", "rb") as f:
        sample_rand = pickle.load(f)
        content_random = sample_rand["memory_perf"]
#    N = 10000
    ks = [1,2,3,4]
    for lp in [True,False]:
        if lp:
            file = lambda k,N: f"{folder}/history_kNN_{k}_N_{N}_lp_0.pkl" 
        else:
            file = lambda k,N: f"{folder}/history_kNN_{k}_N_{N}_no_lp_0.pkl"
        for k_moins_un,name in [(k,file(k,N)) for k in ks]:
            with open(name, "rb") as f:
                sample = pickle.load(f)
                content_imgep = sample["memory_perf"]
            file_names = [f"{image_folder}/comp_ratios_{k_moins_un}_{N}",f"{image_folder}/comp_times_k{k_moins_un}_{N}",f"{image_folder}/comp_count_{k_moins_un}_{N}"]
            if lp:
                file_names = [f+"_lp" for f in file_names]
            else:
                file_names = [f+"_no_lp" for f in file_names]
            comparaison3(content_random, content_imgep, name = file_names, title=f"miss ratios k = {k_moins_un}, {N} iterations")
    ks = [1,2,3,4]
    #exit()
    for k in ks:
        diversity_time_iteration2(content_random,
                                [("imgep no lp",k,f"{folder}/history_kNN_{k}_N_{N}_no_lp_0.pkl")]
                                +[("imgep -lp",k,f"{folder}/history_kNN_{k}_N_{N}_lp_0.pkl")],
                                #+ [("imgep 1 module",k,f"{folder1module}/history_kNN_{k}_N_{N}_no_lp_0")],
                                title = f"comparaison_time_diversity_{k}",
                                folder = image_folder)



    for k in [1,2,3,4]:
        with open(f"{folder}/history_kNN_{k}_N_{N}_no_lp_0.pkl", "rb") as f:
            sample = pickle.load(f)
            content_imgep_no_lp = sample["memory_perf"] 
        with open(f"{folder}/history_kNN_{k}_N_{N}_lp_0.pkl", "rb") as f:
            sample = pickle.load(f)
            content_imgep_lp = sample["memory_perf"]
        #with open(f"{folder1module}/history_kNN_{k}_N_{N}_no_lp_0.pkl", "rb") as f:
        #    sample = pickle.load(f)
        #    content_imgep_no_lp_1module = sample["memory_perf"] 
        #with open(f"data_1module/history_kNN_{k}_N_{N}_lp_0.pkl", "rb") as f:
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
