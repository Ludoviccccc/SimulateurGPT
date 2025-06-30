import json
if __name__ == "__main__":
    folder = ["data","data_weak"]
    folder1module = "data_1module"
    image_folder ="image_comp"
    test_mode = False
    N = int(10000)
    N_init = 1000
    ks = [1,2,3,4]
    file_weak = lambda k,N: f"history_weak_{k}_N_{N}_0.pkl"
    file_imgep_ir = lambda k,N: f"history_kNN_{k}_N_{N}_lp_0.pkl"
    file_imgep_no_ir = lambda k,N: f"history_kNN_{k}_N_{N}_no_lp_0.pkl"
    files = []
    files +=[{"folder":folder[1],"file":file_weak(k,N),"name":f"weak_imgep k={k},N={N}","k":k,"N":N,"type":"weak_imgep"} for k in ks]
    files +=[{"folder":folder[0],"file":file_imgep_ir(k,N),"name":f"imgep_ir k={k},N={N}","k":k,"N":N,"type":"imgep_ir"} for k in ks]
    files +=[{"folder":folder[0],"file":file_imgep_no_ir(k,N),"name":f"imgep_no_ir k={k},N={N}","k":k,"N":N,"type":"imgep_no_ir"} for k in ks]

    random = {"folder":folder1module,
                "N":N,
                "file":f"history_rand_N_{N}_0.pkl",
                "name": "random"}
    config = {"files":files,
              "N_init":N_init,
              "N":N,
              "image_folder":image_folder,
              "random":random}

    with open(f"{image_folder}/config_plots.json","w") as f:
        json.dump(config, f)
