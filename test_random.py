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
#    random.seed(0)
    N = int(100)
    max_len = 500  
    length_programs = 100


    H = History(max_size=1000)
    En = Env(length_programs=length_programs, max_len=max_len)
    imgep = RANDOM(N = N,N_init=N,E = En, H = H)
    imgep()
    #for j in range(1):
    #    print(H.memory_signature["core0"]["bank"][0])
    #    print(H.memory_signature["core1"]["bank"][0])
    #exit()
    def countDDR(H:History):
        def same(string):
            A = np.array(H.memory_signature["core0"][string])
            B = np.array(H.memory_signature["core1"][string])
            C = A==B
            return 1.0*(C) - 1.0*(C)*(A==-1)*(B==-1)
        same_address = same("addr")
        same_bank = same("bank")
        def count_(string):
            G0 = np.array(H.memory_signature["core0"][string])
            G1 = np.array(H.memory_signature["core1"][string])
            n = 20 if string=="addr" else 4
            counts0 = np.array([np.sum(G0[:,:]==item) for item in range(0,n)])
            counts1 = np.array([np.sum(G1[:,:]==item) for item in range(0,n)])
            return counts0, counts1
        counts_addr_0, counts_addr_1 = count_("addr")
        counts_bank_0, counts_bank_1 = count_("bank")
        return same_address,counts_addr_0,counts_addr_1, same_bank, counts_bank_0, counts_bank_1
    
    A = np.array(H.memory_signature["core0"]["addr"])
    B = np.array(H.memory_signature["core1"]["addr"])     
    print(A.shape)
    up = 130
    plt.scatter(range(up), A[0,:up])
    plt.scatter(range(up), B[0,:up])
    for j in range(100):
        xA,yA = j,A[0][j]
        xB,yB = j,B[0][j]
        radiusA = H.memory_signature["core0"]["max_radius"][0][j]
        radiusB = H.memory_signature["core1"]["max_radius"][0][j]
        theta = np.linspace(0, 2*np.pi, 100)
        if radiusA>0:
            xA_circle = xA + radiusA * np.cos(theta)
            yA_circle = yA + radiusA * np.sin(theta)
            plt.plot(xA_circle, yA_circle, 'r-', label=f'Circle (r={radiusA})')
        if radiusB>0:
            xB_circle = xB + radiusB * np.cos(theta)
            yB_circle = yB + radiusB * np.sin(theta)
            plt.plot(xB_circle, yB_circle, 'r-', label=f'Circle (r={radiusB})')
    plt.show()
    same_address,counts_addr_0, counts_addr_1,same_bank, counts_bank_0, counts_bank_1 = countDDR(H)
    plt.figure()
    plt.plot(sum(same_address), label ="random")
    plt.xlabel("cycle")
    plt.legend()
    plt.title("Number of ddr acces at same address by both cores at same cycle")
    plt.savefig("image/figure1")
    plt.show()

#    plt.plot(sum(same_bank), label ="random")
#    plt.xlabel("cycle")
#    plt.legend()
#    plt.title("Number of ddr acces at same bank by both cores at same cycle")
#    plt.savefig("image/figure2")
#    plt.show()
    

    #plt.figure()
    #plt.scatter(range(20),counts_addr_0, label="core0, random")
    #plt.scatter(range(20),counts_addr_1, label="core1, random")
    #plt.grid()
    #plt.title("number of acces to ddr vs addresses")
    #plt.legend()
    #plt.xticks(range(20))
    #plt.savefig("image/figure3")
    #plt.show()

    #print((np.sum(np.array(H.memory_signature["core0"][f"bank{0}"]))))
    sumbank0 = np.array([np.sum(np.array(H.memory_signature["core0"][f"bank{j}"])) for j in range(4)])
    sumbank0_alone = np.array([np.sum(np.array(H.memory_signature["core0_alone"][f"bank{j}"])) for j in range(4)])
    sumbank1 = np.array([np.sum(np.array(H.memory_signature["core1"][f"bank{j}"])) for j in range(4)])
    #print(sumbank0)
    plt.figure()
    plt.bar(range(0,4,1),sumbank0,label="")
    plt.bar(range(4,8,1),sumbank1,label="")
    plt.xticks(range(8),["core0" + f"& bank {j}" for j in range(4)] + ["core1" + f"{j}" for j in range(4)])
    plt.show()


    def times_plot(H:History, data = "delay",core = "core0",name=None):
        time_together = np.array(H.memory_signature[core][data])
        if data=="completion_time":
            time_alone = np.array(H.memory_signature[f"{core}_alone"]["completion_time"])
        for j in range(len(time_together)):
            if data=="completion_time":
                plt.plot(range(length_programs),(time_together[j] - time_alone[j]),".-", label=f"{j} {core}")
            else:
                plt.plot(range(length_programs),time_together[j],".-", label=f"{j} {core}")
            if data=="completion_time":
                plt.title(r"$\Delta$ T"+f" {core}")
            else:
                plt.title(f"{data} {core}")
        plt.legend()
        plt.xticks(range(0,length_programs,5))
        plt.grid()
        if name:
            plt.savefig(name)
        plt.show()
    times_plot(H, core = "core0", name = "image/figure5")
    times_plot(H, core = "core1", name = "image/figure6")

#    times_plot(H, data = "completion_time",core = "core0")
#    times_plot(H, data = "completion_time",core = "core1")

    #for j in range(1):
    time_banka = np.array(H.memory_signature["core0"][f"bank{0}"])
    print("time banka", np.sum(time_banka.sum(axis=0)>=2))

    bank = 0
    core = "core0"

    time_bankb = np.array(H.memory_signature[f"{core}_alone"][f"bank{bank}"])
    plt.bar(np.arange(max_len),time_banka.sum(axis=0), label=f"{core} along with other core")
    plt.bar(np.arange(max_len),time_bankb.sum(axis=0), label=f"{core} alone")
    plt.legend()
    plt.title(f"number of accesses for bank {bank} vs arrival time")
    plt.show()

    simultaneous_access_core0 = np.array([np.sum(np.array(H.memory_signature["core0"][f"bank{j}"])>=2) for j in range(4)])
    simultaneous_access_core1 = np.array([np.sum(np.array(H.memory_signature["core1"][f"bank{j}"])>=2) for j in range(4)])
    simultaneous_access_alone_core0 = np.array([np.sum(np.array(H.memory_signature["core0_alone"][f"bank{j}"])>=2) for j in range(4)])
    plt.figure()
    plt.bar(range(4), simultaneous_access_core0 - simultaneous_access_alone_core0, label=r"$\delta$n core0")
    plt.bar(range(4,8), simultaneous_access_core1, label="core1")
    plt.xticks(range(4), range(4))
    plt.legend()
    plt.title("Number of simultaneous accesses")
    plt.show()

    def times(H:History,core:str):
        times_core = np.array([np.array(H.memory_signature[core]["time"])[j] for j in range(len(H))])
        times_core_alone = np.array([np.array(H.memory_signature[f"{core}_alone"]["time"])[j] for j in range(len(H))])
        return times_core, times_core_alone
    times_core0, times_core0_alone = times(H, "core0")
    times_core1, times_core1_alone = times(H, "core1")
    plt.figure()
    plt.plot(times_core0 - times_core0_alone, label=r"with core 1 - alone")
    plt.title("Execution time for core 0 - Execution time for core 0 alone")
    plt.legend()
    plt.savefig("image/figure8")
    plt.show()

    plt.figure()
    plt.plot(times_core1 - times_core1_alone, label=r"with core 1 - alone")
    plt.xlabel("num experience")
    plt.title("Execution time for core 1 - Execution time for core 1 alone")
    plt.legend()
    plt.savefig("image/figure8")
    plt.show()

    pp = H.memory_signature["core0"]["pending_addr"]
    for k in range(len(pp)):
        for i in range(len(pp[k])):
            if len(pp[i])>0:
                plt.scatter([i]*len(pp[k][i]),pp[k][i])
    plt.ylabel("addresses")
    plt.xlabel("time (cycle)")
    plt.show()
        
    pp = H.memory_signature["core0"]["pending_core_id"]
    for k in range(len(pp)):
        for i in range(len(pp[k])):
            plt.scatter(i,len(pp[k][i]))
        break
    plt.title("number of instructions in ddr queue from core 0")
    plt.ylabel("addresses")
    plt.xlabel("time (cycle)")
    plt.show()
        
