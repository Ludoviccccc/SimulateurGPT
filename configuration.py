import json
if __name__ == "__main__":
    folder = "data"
    folder1module = "data_1module"
    image_folder ="image"
    test_mode = False
    num_addr = 20
    N = int(10000)
    N_init = 1000
    max_len = 50
    periode = 100
    num_bank = 4 # m'est pas variable, a changer dans dossier simulation
    mutation_rate = .1
    modules =   ["time"]
    modules +=   [f"miss_bank_{j}" for j in range(num_bank)]
    modules +=  [f"diff_ratios_bank_{j}" for j in range(num_bank)]
    modules +=  [{"type":"time_diff","core":core} for core in range(2)]
    modules +=  [{"type":"miss_count", "bank":bank} for bank in range(num_bank)]
    #modules += [{"type":"miss_ratios_global"}]
    #modules += [{"type":"miss_ratios_global_time"}]
    dict_modules = [{"type":"miss_ratios","bank":bank, "core":core} for core in [None, 0,1] for bank in range(num_bank)]
    dict_times = [{"type":"time", "core":core,"single":single} for core in range(2) for single in [True, False]]

    ratios_detailled = [{"type":"miss_ratios_detailled","bank":bank,"core":core,"row":row} for core in [None,0,1] for bank in range(num_bank) for row in range((num_addr//16)+1)]
    ks = [1,2,3,4]
    modules = modules + dict_modules + ratios_detailled + dict_times

    config = {"modules":modules,
              "N_init":N_init,
              "N":N,
              "periode":periode,
              "mutation_rate":mutation_rate,
              "max_len":max_len,
              "num_addr":20,
              "num_bank":num_bank,
              "image_folder":image_folder,
              "folder":folder,
              "ks":ks}
    with open(f"{folder}/config.json","w") as f:
        json.dump(config, f)
