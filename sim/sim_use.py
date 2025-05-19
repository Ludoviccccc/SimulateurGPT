import numpy as np
import sys
sys.path.append("../sim")
sys.path.append("../")
import random
from sim.class_mem_sim import DDRMemory, Interconnect, MultiLevelCache
class runpgrms: 
    def __init__(self, core1, core0, max_instr, interconnect, ddr):   
        self.nb_read =0   
        self.interconnect = interconnect
        self.ddr = ddr
        self.max_instr = max_instr  
        
        self.core0 = core0
        self.list_acces_L30 = []    
        self.list_addr0 = []   
        
        self.core1 = core1
        self.list_acces_L31 = []    
        self.list_addr1 = []   
    def eviction(self):
        self.list_acces_L31 = []    
        self.list_addr1 = []   
        self.list_acces_L30 = []    
        self.list_addr0 = []   
    def _execut_instr(self, instr:list[dict], cycle:int):    
        """
        executes a list of instructions. Returns 1 if there is acces to the L3, and 0 else.
        """
        out = -1
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
        else:   
            print("erreur")    
            exit()   
        return out   
    def __call__(self, list_instr0:list[dict], list_instr1:list[dict]):  
        #assert len(list_instr0)>0, "longueur programme"
        #assert len(list_instr1)>0, "longueur programme"
        #assert len(self.list_addr0)==0
        #assert len(self.list_addr1)==0
        #assert len(list_instr0)==len(list_instr1)  
        len_ = 0
        for j in range(max(len(list_instr0), len(list_instr1))):
#  print(f"\n========== CYCLE {j} ==========") 
            if j <len(list_instr0):
                out = self._execut_instr(list_instr0[j], cycle=j)
                self.list_acces_L30.append(out)   
                self.list_addr0.append(list_instr0[j]["addr"]*out+(1-out)*(-1))
                #print(list_instr0[j]["addr"]*out+(1-out)*(-1))
                len_+=1
            if j <len(list_instr1):
                out = self._execut_instr(list_instr1[j], cycle=j)
                self.list_acces_L31.append(out)   
                #self.list_addr1.append(list_instr1[j]["addr"])   

                self.list_addr1.append(list_instr1[j]["addr"]*out+(1-out)*(-1))
                len_+=1
            self.interconnect.tick()
            output_tick = self.ddr.tick()    
            if type(output_tick)==dict:
                print("output_tick", output_tick)
            #print("row buffer",self.ddr.bank_row_buffers)
            if len_==0:
                print("erreur")
                exit()
    def acces_history(self):   
        a = np.zeros(self.max_instr)   
        b = np.zeros(self.max_instr)   
        a[:len(self.list_acces_L30)] = self.list_acces_L30
        b[:len(self.list_acces_L31)] = self.list_acces_L31
        return a*b
    def addr_core(self,j):
        a = np.zeros(self.max_instr) - 1
        if j==0:
            a[:len(self.list_addr0)] = self.list_addr0
        elif j==1:
            a[:len(self.list_addr1)] = self.list_addr1
        return a
    def addr_obs(self):
        return {"addr":np.concatenate((self.addr_core(0), self.addr_core(1)), axis =0)}
    def addr_history(self):
        a = self.addr_core(0)
        b = self.addr_core(1)
        return a==b
    def same_acces(self):
        out = self.addr_history()*self.acces_history()*1.0
        return out
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
def make_random_paire_list_instr(length:int=50)->dict:
    assert type(length) == int
    length = 50
    instructions0 = make_random_list_instr(length=length, core=0)
    instructions1 = make_random_list_instr(length=length, core=1)
    return  {"core0": [instructions0],"core1":[instructions1]}

