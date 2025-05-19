import sys
import random
sys.path.append("../")
sys.path.append("../sim")
from sim.sim_use import runpgrms, make_random_list_instr
def random_exploration(core0, core1,interconnect,ddr, budget:int=50, max_instr:int=50):
    program = runpgrms(core0, core1, max_instr, interconnect, ddr)
    list_intersection = []
    list_obj = []
    for i in range(budget):
        instructions0 = make_random_list_instr(length=random.randint(5,max_instr), core=0)
        instructions1 = make_random_list_instr(length=random.randint(5,max_instr), core=1)
        program(instructions0, instructions1)
        list_intersection.append(program.same_acces())
        list_obj.append(program.addr_obs())
        print("acces L3 core 0", program.list_acces_L30)
        print("acces L3 core 1", program.list_acces_L31)
        program.eviction()
    return list_intersection, list_obj
