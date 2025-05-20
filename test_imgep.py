from sim.class_mem_sim import Interconnect, MultiLevelCache
from sim.ddr import DDRMemory
import random
import time
import numpy as np
from sim.sim_use import runpgrms, make_random_list_instr, make_random_paire_list_instr
from exploration.random.func import random_exploration
from exploration.imgep.history import History
from exploration.imgep.goal_generator import GoalGenerator
from exploration.imgep.OptimizationPolicy import OptimizationPolicy, OptimizationPolicykNN
from exploration.imgep.mutation import mutate_paire_instructions 

import matplotlib.pyplot as plt


class Env:
    def __init__(self, program_trans):
        self.program_trans = program_trans
    def __call__(self, parameter:dict):
        self.program_trans(parameter["core0"][0], parameter["core1"][0])
        observation = self.program_trans.addr_obs()
        return observation
    def eviction(self):
        self.program_trans.eviction()



class IMGEP:
    def __init__(self,N:int, N_init:int,E:Env,H:History, G:GoalGenerator, Pi:OptimizationPolicy, periode:int = 1):
        """
        N: int. The experimental budget
        N_init: int. Number of experiments at random
        H: History. Buffer containing codes and signature pairs
        G: GoalGenerator.
        Pi: OptimizationPolicy.
        """
        self.N = N
        self.env = E
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
        self.periode = periode
    def __call__(self):
        for i in range(self.N):
            if i<self.N_init:
                parameter = make_random_paire_list_instr()
            else:
                #Sample target goal
                if i%self.periode==0:
                    goal = self.G()
                #policy selects a parameter
                parameter = self.Pi(goal,self.H)
            observation = self.env(parameter)
            self.H.store({"program":parameter, "addr":[observation["addr"]]})
            self.env.eviction()
if __name__=="__main__":

    # Simulation setup
    
#    random.seed(0)


    N = int(1000)
    
    ddr = DDRMemory()
    interconnect = Interconnect(ddr, delay=5, bandwidth=4)
    l1_conf = {'size': 32,  'line_size': 4, 'assoc': 2}
    l2_conf = {'size': 128, 'line_size': 4, 'assoc': 4}
    l3_conf = {'size': 512, 'line_size': 4, 'assoc': 8}
    core0 = MultiLevelCache(0, l1_conf, l2_conf, l3_conf, interconnect)
    core1 = MultiLevelCache(1, l1_conf, l2_conf, l3_conf, interconnect)
    program = runpgrms(core0, core1, 50, interconnect, ddr)


    H = History(max_size=1000)
    En = Env(program)
    G = GoalGenerator(50, 20)
    P = OptimizationPolicykNN(k=5,mutation_rate =0.1)

    def countL3(H:History):
        A = np.array(H.memory_signature["addr"])[:,:50]
        B = np.array(H.memory_signature["addr"])[:,50:]
        C = A==B
        D1 = 1.0*(C) - 1.0*(C)*(A==-1)*(B==-1)
        E = A*D1
        G = (A+1)*C
        counts= np.array([[np.sum(G[:,j]==item) for item in range(1,21)] for j in range(G.shape[1])])


        G = np.array(H.memory_signature["addr"])
        counts_per_addr = np.array([np.sum(G[:,:]==item) for item in range(0,20)])
        return counts_per_addr,D1,counts

    imgep = IMGEP(N,200,En, H, G, P)
    imgep()
    counts_per_addr_imgep,D1,counts_per_addr_per_cycle_imgep = countL3(H)

    
    #H.purge()

    ddr = DDRMemory()
    interconnect = Interconnect(ddr, delay=5, bandwidth=4)
    core0 = MultiLevelCache(0, l1_conf, l2_conf, l3_conf, interconnect)
    core1 = MultiLevelCache(1, l1_conf, l2_conf, l3_conf, interconnect)
    program = runpgrms(core0, core1, 50, interconnect, ddr)

    H = History(max_size=1000)
    En = Env(program)
    G = GoalGenerator(50, 20)
    P = OptimizationPolicykNN(k=5,mutation_rate =0.1)

    Rand = IMGEP(N,N,En, H, G, P)
    Rand()
    counts_per_addr_rand, D2,counts_per_addr_per_cycle_rand = countL3(H)

    plt.figure()
    plt.plot(sum(D1), label="imgep")
    plt.plot(sum(D2), label ="random")
    plt.xlabel("cycle")
    plt.title("Number of acces by both cores at same cycle")
    plt.legend()
    plt.savefig("image/figure1")
    plt.show()


    plt.figure()
    plt.plot(range(20), np.mean(counts_per_addr_per_cycle_imgep, axis =0), label="imgep")
    plt.plot(range(20), np.mean(counts_per_addr_per_cycle_rand, axis =0), label="rand")
    plt.legend()
    plt.title("average number of time ddr is accesed by both cores")
    plt.savefig("image/figure2")
    plt.show()
    
    plt.figure()
    plt.scatter(range(20),counts_per_addr_imgep, label="imgep")
    plt.scatter(range(20),counts_per_addr_rand, label="rand")
    plt.grid()
    plt.title("number of acces to ddr vs address")
    plt.xlabel("addr")
    plt.legend()
    plt.xticks(range(0,20))
    plt.savefig("image/figure3")
    plt.show()
