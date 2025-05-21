from sim.class_mem_sim import Interconnect, MultiLevelCache
from sim.ddr import DDRMemory
import random
import time
import numpy as np
from sim.sim_use import runpgrms, make_random_list_instr, make_random_paire_list_instr
from exploration.random.func import random_exploration
from exploration.imgep.history import History, History2
from exploration.imgep.goal_generator import GoalGenerator
from exploration.imgep.OptimizationPolicy import OptimizationPolicy, OptimizationPolicykNN
from exploration.imgep.mutation import mutate_paire_instructions 

import matplotlib.pyplot as plt


class Env:
    def __init__(self,
                l1_conf = {'size': 32,  'line_size': 4, 'assoc': 2},
                l2_conf = {'size': 128, 'line_size': 4, 'assoc': 4},
                l3_conf = {'size': 512, 'line_size': 4, 'assoc': 8},
                length_programs = 50,
                max_len=350):
        self.l1_conf = l1_conf
        self.l2_conf = l2_conf
        self.l3_conf = l3_conf
        self.max_len = max_len
        self.length_programs = length_programs
    def __call__(self, parameter:dict):
        ddr = DDRMemory()
        interconnect = Interconnect(ddr, delay=5, bandwidth=4)
        core0 = MultiLevelCache(0, self.l1_conf, self.l2_conf, self.l3_conf, interconnect)
        core1 = MultiLevelCache(1, self.l1_conf, self.l2_conf, self.l3_conf, interconnect)
        program = runpgrms(core0, core1, self.length_programs, interconnect, ddr, max_len=max_len)
        program(parameter["core0"][0], parameter["core1"][0])
        return {"core0":program.out0, "core1":program.out1}

class RANDOM:
    def __init__(self,N:int, N_init:int,E:Env,H:History2):
        """
        N: int. The experimental budget
        N_init: int. Number of experiments at random
        H: History. Buffer containing codes and signature pairs
        """
        self.N = N
        self.env = E
        self.H = H
        self.N_init = N_init
    def __call__(self):
        for i in range(self.N):
            if i<self.N_init:
                parameter = make_random_paire_list_instr()
            self.H.store({"program":parameter}|self.env(parameter))
if __name__=="__main__":
#    random.seed(0)
    N = int(1000)
    max_len = 350  
    length_programs = 100


    H = History2(max_size=1000)
    En = Env(length_programs=length_programs, max_len=max_len)
    imgep = RANDOM(N = 10,N_init=10,E = En, H = H)
    imgep()
    for j in range(10):
        print(H.memory_program["core0"][j][0])
    def countDDR(H:History2):
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
    

    same_address,counts_addr_0, counts_addr_1,same_bank, counts_bank_0, counts_bank_1 = countDDR(H)
    plt.figure()
    plt.plot(sum(same_address), label ="random")
    plt.xlabel("cycle")
    plt.legend()
    plt.title("Number of ddr acces at same address by both cores at same cycle")
    plt.savefig("image/figure1")
    plt.show()

    plt.plot(sum(same_bank), label ="random")
    plt.xlabel("cycle")
    plt.legend()
    plt.title("Number of ddr acces at same bank by both cores at same cycle")
    plt.savefig("image/figure2")
    plt.show()
    

    plt.figure()
    plt.scatter(range(20),counts_addr_0, label="core0, random")
    plt.scatter(range(20),counts_addr_1, label="core1, random")
    plt.grid()
    plt.title("number of acces to ddr vs addresses")
    plt.legend()
    plt.xticks(range(20))
    plt.savefig("image/figure3")
    plt.show()


    plt.figure()
    plt.scatter(range(4),counts_bank_0, label="core0, random")
    plt.scatter(range(4),counts_bank_1, label="core1, random")
    plt.grid()
    plt.title("number of acces to ddr vs bank")
    plt.legend()
    plt.xticks(range(4))
    plt.savefig("image/figure4")
    plt.show()



    def times_plot(H:History2, name="image/figure5"):
        tab_delay0 = np.array(H.memory_signature["core0"]["delay"])
        tab_delay1 = np.array(H.memory_signature["core1"]["delay"])
        for j in range(len(tab_delay0)):
            plt.plot(range(length_programs),tab_delay0[j], label=f"{j} core 0")
            plt.plot(range(length_programs),tab_delay1[j], label=f"{j} core 1")
            plt.title("delays")
        plt.legend()
        if name:
            plt.savefig(name)
        plt.show()
    times_plot(H)
