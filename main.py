from sim.class_mem_sim import Interconnect, MultiLevelCache
from sim.ddr import DDRMemory
import random
import time
import numpy as np
from sim.sim_use import runpgrms, make_random_list_instr
from exploration.random.func import random_exploration
import matplotlib.pyplot as plt





if __name__=="__main__":

    # Simulation setup
    
#    random.seed(0)
    
    ddr = DDRMemory()
    interconnect = Interconnect(ddr, delay=5, bandwidth=4)
    l1_conf = {'size': 32, 'line_size': 4, 'assoc': 2}
    l2_conf = {'size': 128, 'line_size': 4, 'assoc': 4}
    l3_conf = {'size': 512, 'line_size': 4, 'assoc': 8}
    core0 = MultiLevelCache(0, l1_conf, l2_conf, l3_conf, interconnect)
    core1 = MultiLevelCache(1, l1_conf, l2_conf, l3_conf, interconnect)
    program = runpgrms(core0, core1, 50, interconnect, ddr)
    length = 30
    instr0 = make_random_list_instr(length=length, core=0)
    instr1 = make_random_list_instr(length=length, core=1)
#    print(instructions0)
    #instr0 = [{'type': 'r', 'addr': j, 'func': lambda val: None, 'core': 0} for j in list(range(20))+list(range(17,20))]
    #instr1 = [{'type': 'r', 'addr': j, 'func': lambda val: None, 'core': 1} for j in range(20)]
    #instr1 = []
    #program(instructions0, instructions1)
    program(instr0, instr1)
    a = program.addr_core(0)
    b = program.addr_core(1)
    o = program.addr_obs()["addr"]
    print(o[:50])
    print(o[50:])
#    print(program.list_acces_ddr0)
    print("list acces ddr 0", program.list_acces_ddr0)
    print("reorder",program.reorder())
    print("out0",program.out0)
    exit()
    print("difference", sum(a != b))
    print("addr core0", program.addr_core(0))
    print("addr core1", program.addr_core(1))

#    print(len(program.addr_obs()))
#
#    exit()
    # Report results
#    print(core0.stats())
    #Descripteur comme un vecteur binaire qui renseigne sur l(acces (1) ou non (0) à une meme addresse pour chaque paire d'instruction au meme cycle
    print("same acces",program.same_acces())

    ddr = DDRMemory()
    interconnect = Interconnect(ddr, delay=5, bandwidth=4)
    l1_conf = {'size': 32, 'line_size': 4, 'assoc': 2}
    l2_conf = {'size': 128, 'line_size': 4, 'assoc': 4}
    l3_conf = {'size': 512, 'line_size': 4, 'assoc': 8}
    core0 = MultiLevelCache(0, l1_conf, l2_conf, l3_conf, interconnect)
    core1 = MultiLevelCache(1, l1_conf, l2_conf, l3_conf, interconnect)
    list_intersection,list_obj = random_exploration(core0, core1, interconnect, ddr,1000, 50)
    for ob in list_intersection:
        plt.plot(range(0,len(list_intersection[0])), ob)
    plt.show()
    #print("liste des observations", list_obj)
