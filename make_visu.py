
import pickle
from visu import diversity_time_iteration2
from visu2 import comparaison3, comparaison_ratios_iterations, comparaison_ratios_global_iterations
from exploration.imgep.intrinsic_reward import IR
import json
import sys
import os
if __name__=="__main__":
    #np.random.seed(0)
    folder1module = "data_1module"
    with open(sys.argv[1],"rb") as f:
        config = json.load(f)
    print("config keys", config.keys())
    N = config["N"]
    N_init = config["N_init"]
    image_folder = config["image_folder"]
    files = config["files"]
    random = config["random"]
    num_bank = config["num_bank"]
    num_addr = config["num_addr"]
    with open(os.path.join(random["folder"],random["file"]),"rb") as f:
        sample = pickle.load(f)
    content_random = sample["memory_perf"]


    contents_ = []
    for data in files:
        with open(os.path.join(data["folder"],data["file"]), "rb") as f:
            sample = pickle.load(f)
            content = sample["memory_perf"]
            contents_.append((data["name"],content,data["k"]))
        comparaison3(content_random, 
                     content, 
                     name = [f"{image_folder}/{nn}_{data['type']}_{data['k']}_{N}" for nn in ["ratios","time"]], 
                     title=[f"{name} k = {data['k']}, {data['N']} iterations" for name in ["miss ratios", "time"]],num_bank=num_bank, num_row = num_addr//16)
    for k_ in [1,2,3,4]:
        diversity_time_iteration2(content_random,
                            [(data["name"],data["k"],f"{data['folder']}/{data['file']}") for data in files if data["k"]==k_],
                           title = f"comparaison_time_diversity_{k_}",
                           folder = image_folder)




        comparaison_ratios_iterations([(a[0],a[1]) for a in contents_ if a[2]==k_] + [("random", content_random)],
                                     name = f"{image_folder}/comp_ratios_iteration_{k_}_{N}", k = k_)
        comparaison_ratios_global_iterations([(a[0],a[1]) for a in contents_ if a[2]==k_] + [("random", content_random)],
                                            name = f"{image_folder}/comp_global_ratios_iteration_{k_}_{N}", k = k_)
