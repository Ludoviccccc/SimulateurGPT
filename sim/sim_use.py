import numpy as np
import sys
sys.path.append("../sim")
sys.path.append("../")
import random
from sim.class_mem_sim import Interconnect, MultiLevelCache
from sim.ddr import DDRMemory
import matplotlib.pyplot as plt
class runpgrms: 
    def __init__(self, core0, core1, interconnect, ddr, num_banks = 4):   
        self.nb_read =0   
        self.interconnect = interconnect
        self.ddr = ddr
        self.num_banks = num_banks
        
        self.core0 = core0
        self.list_acces_ddr0 = []    
        self.list_best_request = []    
        self.list_address0 = []   
        
        self.core1 = core1
        self.list_acces_ddr1 = []    
        self.list_best_request1 = []    
        self.list_address1 = []   
        #self.max_len = max_len
        self.miss_count = np.zeros(self.num_banks) 
        self.hits_count = np.zeros(self.num_banks)
        self.ratios = None
        self.compl_time_core0 = 0
        self.compl_time_core1 = 0


    def _execut_instr(self, instr:list[dict], cycle:int):    
        """
        executes a list of instructions. Returns 1 if there is acces to the L3, and 0 else.
        """
        #out = -1
        #print("instr:",instr)
        #exit()
        if instr["type"]=="r": 
            if instr["core"]==0:    
                out = self.core0.read(instr["addr"], instr["func"]) 
                #print("fin")
                #exit()
            elif instr["core"]==1:  
                out = self.core1.read(instr["addr"], instr["func"])    
        elif instr["type"]=="w":    
            if instr["core"]==0:    
                out = self.core0.write(instr["addr"], instr["value"])  
            elif instr["core"]==1:  
                out = self.core1.write(instr["addr"], instr["value"])  
        #else:   
        #    print("erreur")    
        #    exit()   
        return out   
    def __call__(self, list_instr0:list[dict], list_instr1:list[dict]):  
        len_ = 0
        k =1
        for j in range(100*max(len(list_instr0), len(list_instr1))):
#  print(f"\n========== CYCLE {j} ==========") 
            if j <len(list_instr0):
                out = self._execut_instr(list_instr0[j], cycle=j)
                self.list_acces_ddr0.append(out)   
                self.list_address0.append(list_instr0[j]["addr"]*out+(1-out)*(-1))
                len_+=1
            if j <len(list_instr1):
                out = self._execut_instr(list_instr1[j], cycle=j)
                self.list_acces_ddr1.append(out)   
                self.list_address1.append(list_instr1[j]["addr"]*out+(1-out)*(-1))
                len_+=1
            self.interconnect.tick()
            output_tick = self.ddr.tick()    
            if type(output_tick)==dict:
                self.list_best_request.append(output_tick)
                #print(k,"output_tick", output_tick)
                k+=1
            if len_==0:
                print("erreur")
                exit()
        self.reorder()
    def reorder(self):
        hits = np.zeros(self.num_banks)
        miss = np.zeros(self.num_banks)
        hits_tab = np.zeros((2,self.num_banks))
        miss_tab = np.zeros((2,self.num_banks))
        for d in self.list_best_request:
            self.miss_count[d["bank"]]+=1*d["status"]=="ROW MISS"
            self.hits_count[d["bank"]]+=1*d["status"]=="ROW HIT"
            if d["status"]=="ROW MISS":
                miss[d["bank"]] +=1
                miss_tab[d["row"],d["bank"]] +=1
            else:
                hits[d["bank"]] +=1
                hits_tab[d["row"],d["bank"]] +=1
            if d["core"]==0:
                self.compl_time_core0 = max(self.compl_time_core0,d["completion_time"])
            elif d["core"]==1:
                self.compl_time_core1 = max(self.compl_time_core1,d["completion_time"])
            else:
                print("erreur")
                exit()
        denominator = miss + hits
        denominator[denominator==0] = -1
        self.ratios = miss/(denominator)
        self.ratios[self.ratios<0] = -1

        denominator_tab  = miss_tab + hits_tab
        denominator_tab[denominator_tab==0] = -1
        self.ratios_tab = miss_tab/(denominator_tab)
        self.ratios_tab[self.ratios_tab<0] = -1
def make_random_list_instr(length = 5, core = "0"):
    out = []
    for j in range(length):
        addr = random.randint(0, 20)    
        if random.random() < .2:   
            out.append({"type":"w",
                         "addr":addr,  
                         "value":random.randint(0, 1000),  
                         "core":core}) 
        else:  
             out.append({"type":"r",
            "addr":addr,  
            "func":lambda val: None,
            "core":core}) 
    return out  
def make_random_paire_list_instr(length:int=50,length2:int=None)->dict:
    assert type(length) == int
    if not length2:
        length2 = length
    instructions0 = make_random_list_instr(length=length, core=0)
    instructions1 = make_random_list_instr(length=length2, core=1)
    return  {"core0": [instructions0],"core1":[instructions1]}

