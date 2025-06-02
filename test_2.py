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
    random.seed(0)
    N = int(100)
    max_len = 500  
    length_programs = 100


    H = History(max_size=1000)
    H2 = History(max_size=1000)
    En = Env(length_programs=length_programs, max_len=max_len)
    imgep = RANDOM(N = N,E = En, H = H, H2 = H2)
    imgep()
    content = H.present_content()
    content2 = H2.present_content()

    fig, axs = plt.subplots(4,4, figsize = (15,10), layout='constrained')
    for j in range(4):
        axs[j,0].hist(content["miss_ratios"][:,j] - content["miss_ratios_core0"][:,j],bins="auto")
        axs[j,0].set_xlabel(f"ratio[bank{j+1},(S_0,S_1)] - ratio[bank{j+1},(S_0,)]")
        axs[j,0].set_title("row miss hits ratio difference")

        axs[j,1].hist(content["miss_ratios"][:,j], label="core 0 and 1 together", alpha=.5)
        axs[j,1].hist(content["miss_ratios_core0"][:,j], label="core 0 alone", alpha=.5)
        axs[j,1].set_xlabel(f"miss ratios bank {j}")
        axs[j,1].set_title(f"miss ratios distribution")


        axs[j,2].scatter(content["miss_ratios_core0"][:,j],  content["miss_ratios"][:,j])
        axs[j,2].set_xlabel("(S_0,)")
        axs[j,2].set_ylabel("(S_0,S_1)")
        axs[j,2].axline(xy1=(0, 0), slope=1, color='r', lw=2)
        axs[j,2].set_title(f"miss ratios bank {j+1}")


        axs[j,3].scatter(content["miss_ratios"][:,j], content2["miss_ratios"][:,j])
        axs[j,3].set_xlabel("run 1")
        axs[j,3].set_ylabel("run 2")
        axs[j,3].set_title(f"miss ratios,bank {j+1} two runs")

    plt.savefig("image/miss_ratios")
    plt.show()
