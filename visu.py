import random
import time
import numpy as np
from exploration.random.func import RANDOM, Env
from exploration.history import History
import matplotlib.pyplot as plt

def representation(content, content2 = None):
    if content2:
        fig, axs = plt.subplots(4,4, figsize = (15,10), layout='constrained')
    else:
        fig, axs = plt.subplots(4,3, figsize = (15,10), layout='constrained')
    for j in range(4):
        axs[j,0].hist(content["miss_ratios"][:,j] - content["miss_ratios_core0"][:,j],bins="auto")
        axs[j,0].set_xlabel(f"ratio[bank{j+1},(S_0,S_1)] - ratio[bank{j+1},(S_0,)]")
        axs[j,0].set_title("row miss hits ratio difference")

        bins = np.arange(-1.0,1.0,0.1)
        axs[j,1].hist(content["miss_ratios"][:,j], label="core 0 and 1 together", alpha=.5, bins=bins )
        axs[j,1].hist(content["miss_ratios_core0"][:,j], label="core 0 alone", alpha=.5,    bins=bins )
        axs[j,1].hist(content["miss_ratios_core1"][:,j], label="core 1 alone", alpha=.5,    bins=bins )
        axs[j,1].set_xlabel(f"miss ratios bank {j}")
        axs[j,1].set_title(f"miss ratios histogram")
        axs[j,1].legend()


        axs[j,2].scatter(content["miss_ratios_core0"][:,j],  content["miss_ratios"][:,j],label="(S_0,)")
        axs[j,2].scatter(content["miss_ratios_core1"][:,j],  content["miss_ratios"][:,j],label="(,S_1)")
        axs[j,2].set_xlabel("miss ratio alone")
        axs[j,2].set_ylabel("(S_0,S_1)")
        axs[j,2].axline(xy1=(0, 0), slope=1, color='r', lw=2)
        axs[j,2].set_title(f"miss ratios bank {j+1}")
        axs[j,2].legend()
        if content2:
            axs[j,3].scatter(content["miss_ratios"][:,j], content2["miss_ratios"][:,j])
            axs[j,3].set_xlabel("run 1")
            axs[j,3].set_ylabel("run 2")
            axs[j,3].set_title(f"miss ratios,bank {j+1} two runs")

    plt.savefig("image/miss_ratios")
    plt.show()

    fig, axs = plt.subplots(3,2, figsize = (15,10), layout='constrained')
    axs[0,0].scatter(content["time_core0_alone"],content["time_core0_together"])
    axs[0,0].axline(xy1=(0, 0), slope=1, color='r', lw=2)
    axs[0,0].set_xlabel("time_core0_alone")
    axs[0,0].set_ylabel("time_core0_together")
    axs[0,1].scatter(content["time_core1_alone"],content["time_core1_together"], alpha = .5)
    axs[0,1].axline(xy1=(0, 0), slope=1, color='r', lw=2)
    axs[0,1].set_xlabel("time_core1_alone")
    axs[0,1].set_ylabel("time_core1_together")


    axs[1,0].hist(content["time_core0_together"] - content["time_core0_alone"], bins="auto")
    axs[1,0].set_xlabel("together - alone")
    axs[1,1].hist(content["time_core1_alone"]-content["time_core1_together"], bins="auto")
    axs[1,1].set_xlabel("together - alone")

    axs[2,0].scatter(content["time_core0_together"],content["time_core1_together"])
    axs[2,0].set_xlabel("time_core0_together")
    axs[2,0].set_ylabel("time_core1_together")

    plt.savefig("image/time")
    plt.show()


def comparaison(content_random, content_imgep = None):
    fig, axs = plt.subplots(4,3, figsize = (15,10), layout='constrained')
    for j in range(4):
        bins = np.arange(-1.0,1.0,0.1)
        axs[j,0].hist(content_random["miss_ratios"][:,j] - content_random["miss_ratios_core0"][:,j],  bins=bins,alpha = .5, label="random")
        axs[j,0].hist(content_imgep["miss_ratios"][:,j] - content_imgep["miss_ratios_core0"][:,j],bins=bins,alpha = .5, label="imgep")
        axs[j,0].set_xlabel(f"ratio[bank{j+1},(S_0,S_1)] - ratio[bank{j+1},(S_0,)]")
        axs[j,0].set_title("row miss hits ratio difference")
        axs[j,0].legend()

        axs[j,1].scatter(content_random["miss_ratios_core0"][:,j],  content_random["miss_ratios"][:,j],  label="(S_0,) random")
        axs[j,1].scatter(content_random["miss_ratios_core1"][:,j],  content_random["miss_ratios"][:,j],  label="(,S_1) random")
        axs[j,1].scatter(content_imgep["miss_ratios_core0"][:,j],  content_imgep["miss_ratios"][:,j],label="(S_0,) imgep")
        axs[j,1].scatter(content_imgep["miss_ratios_core1"][:,j],  content_imgep["miss_ratios"][:,j],label="(,S_1) imgep")
        axs[j,1].set_xlabel("miss ratio alone")
        axs[j,1].set_ylabel("(S_0,S_1)")
        axs[j,1].axline(xy1=(0, 0), slope=1, color='r', lw=2)
        axs[j,1].set_title(f"miss ratios bank {j+1}")
        axs[j,1].legend()

    plt.savefig("image/comparaison_miss_ratios")
    plt.show()

    fig, axs = plt.subplots(3,2, figsize = (15,10), layout='constrained')
    axs[0,0].scatter(content_random["time_core0_alone"],content_random["time_core0_together"], label="random")
    axs[0,0].scatter(content_imgep["time_core0_alone"],content_imgep["time_core0_together"], label="imgep")
    axs[0,0].axline(xy1=(0, 0), slope=1, color='r', lw=2)
    axs[0,0].set_xlabel("time_core0_alone")
    axs[0,0].set_ylabel("time_core0_together")
    axs[0,0].legend()

    axs[0,1].scatter(content_random["time_core1_alone"],content_random["time_core1_together"], alpha = .5, label="random")
    axs[0,1].scatter(content_imgep["time_core1_alone"],content_imgep["time_core1_together"], alpha = .5, label="imgep")
    axs[0,1].axline(xy1=(0, 0), slope=1, color='r', lw=2)
    axs[0,1].set_xlabel("time_core1_alone")
    axs[0,1].set_ylabel("time_core1_together")
    axs[0,1].legend()



    axs[1,0].hist(content_random["time_core0_together"] - content_random["time_core0_alone"], bins="auto",alpha=.5, label="random")
    axs[1,0].hist(content_imgep["time_core0_together"] - content_imgep["time_core0_alone"], bins="auto",alpha=.5, label="imgep")
    axs[1,0].set_xlabel("time[together] - time[alone]")
    axs[1,0].legend()
    axs[1,1].hist(content_random["time_core1_together"]-content_random["time_core1_alone"], bins="auto", label="random")
    axs[1,1].hist(content_imgep["time_core1_together"]-content_imgep["time_core1_alone"],   bins="auto", label="imgep")
    axs[1,1].set_xlabel("time[together] - time[alone]")
    axs[1,1].legend()

    axs[2,0].scatter(content_random["time_core0_together"],content_random["time_core1_together"], label="random")
    axs[2,0].scatter(content_imgep["time_core0_together"],content_imgep["time_core1_together"], label="imgep")
    axs[2,0].set_xlabel("time_core0_together")
    axs[2,0].set_ylabel("time_core1_together")
    axs[2,0].legend()

    plt.savefig("image/comparaison_time")
    plt.show()
if __name__=="__main__":
    random.seed(0)
    N = int(10)
    max_len = 500  
    length_programs = 100

    H = History(max_size=1000)
    H2 = History(max_size=1000)
    En = Env(length_programs=length_programs, max_len=max_len)
    rand = RANDOM(N = N,E = En, H = H, H2 = H2)
    rand()
    content = H.present_content()
    content2 = H2.present_content()
    representation(content, content2)
    representation(content)
