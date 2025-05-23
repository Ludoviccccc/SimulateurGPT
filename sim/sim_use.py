import numpy as np
import sys
sys.path.append("../sim")
sys.path.append("../")
import random
from sim.class_mem_sim import Interconnect, MultiLevelCache
from sim.ddr import DDRMemory
import matplotlib.pyplot as plt
class runpgrms: 
    def __init__(self, core0, core1, max_instr, interconnect, ddr, max_len =350):   
        self.nb_read =0   
        self.interconnect = interconnect
        self.ddr = ddr
        self.max_instr = max_instr  
        
        self.core0 = core0
        self.list_acces_ddr0 = []    
        self.list_best_request = []    
        self.list_address0 = []   
        
        self.core1 = core1
        self.list_acces_ddr1 = []    
        self.list_best_request1 = []    
        self.list_address1 = []   
        self.max_len = max_len

        self.out0 = {"addr":-np.ones(self.max_len),

                    "addr2": -np.ones(self.max_instr),
                    "bank":-np.ones(self.max_len),
                    "bank0":-np.zeros(self.max_len),
                    "bank1":-np.zeros(self.max_len),
                    "bank2":-np.zeros(self.max_len),
                    "bank3":-np.zeros(self.max_len),
                    "delay":-np.ones(self.max_instr),
                    "completion_time":-np.ones(self.max_instr),
                    "status":-np.ones(self.max_len),
                    "time":0,
                    "min_time":-np.ones(self.max_instr),
                    "max_time":-np.ones(self.max_instr),
                    "min_addr":-np.ones(self.max_instr),
                    "max_addr":-np.ones(self.max_instr),
                    "max_radius":-np.ones(self.max_instr),
                    "pending_addr":[],
                    "pending_core_id":[],
                    }
        self.out1 = {"addr":-np.ones(self.max_len),
                    "addr2":-np.ones(self.max_instr),
                    "bank":-np.ones(self.max_len),
                    "bank0":-np.zeros(self.max_len),
                    "bank1":-np.zeros(self.max_len),
                    "bank2":-np.zeros(self.max_len),
                    "bank3":-np.zeros(self.max_len),
                    "delay":-np.ones(self.max_instr),
                    "completion_time":-np.ones(self.max_instr),
                    "status":-np.ones(self.max_len),
                    "time":0,
                    "min_time":-np.ones(self.max_instr),
                    "max_time":-np.ones(self.max_instr),
                    "min_addr":-np.ones(self.max_instr),
                    "max_addr":-np.ones(self.max_instr),
                    "max_radius":-np.ones(self.max_instr),
                    "pending_addr":[],
                    "pending_core_id":[],
                    }


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
                print(k,"output_tick", output_tick)
                k+=1
            if len_==0:
                print("erreur")
                exit()
        self.reorder()
    def reorder(self):
        #var = {
        for d in self.list_best_request:
            if d["core"]==0:
                self.out0["addr"][d["arrival_time"]] = d["addr"]
                self.out0["addr2"][d["emmission_cycle"]] = d["addr"]
                self.out0["min_time"][d["emmission_cycle"]] = d["min_time"]
                self.out0["max_time"][d["emmission_cycle"]] = d["max_time"]
                self.out0["max_radius"][d["emmission_cycle"]] = d["max_radius"]
                self.out0["min_addr"][d["emmission_cycle"]] = d["min_addr"]
                self.out0["max_addr"][d["emmission_cycle"]] = d["max_addr"]
                self.out0["bank"][d["arrival_time"]] = d["bank"]
                self.out0["delay"][d["emmission_cycle"]] = d["emmission_cycle"]
                self.out0["completion_time"][d["emmission_cycle"]] = d["emmission_cycle"]
                self.out0["status"][d["arrival_time"]] = 1*d["status"]=="ROW MISS"
                self.out0[f"bank{d['bank']}"][d["arrival_time"]] +=1
                self.out0["time"] = max(self.out0["time"], d["completion_time"]) 
                self.out0["pending_addr"].append(d["pending_addr"])
                self.out0["pending_core_id"].append(d["pending_core_id"])
            elif d["core"]==1:
                self.out1["addr"][d["arrival_time"]] = d["addr"]
                self.out1["addr2"][d["emmission_cycle"]] = d["addr"]
                self.out1["min_time"][d["emmission_cycle"]] = d["min_time"]
                self.out1["max_time"][d["emmission_cycle"]] = d["max_time"]
                self.out1["max_radius"][d["emmission_cycle"]] = d["max_radius"]
                self.out1["min_addr"][d["emmission_cycle"]] = d["min_addr"]
                self.out1["max_addr"][d["emmission_cycle"]] = d["max_addr"]
                self.out1["bank"][d["arrival_time"]] = d["bank"]
                self.out1[f"bank{d['bank']}"][d["arrival_time"]] +=1
                self.out1["delay"][d["emmission_cycle"]] = d["emmission_cycle"]
                self.out1["completion_time"][d["emmission_cycle"]] = d["emmission_cycle"]
                self.out1["status"][d["arrival_time"]] = 1*d["status"]=="ROW MISS"
                self.out1["time"] = max(self.out1["time"], d["completion_time"]) 
                self.out1["pending_addr"].append(d["pending_addr"])
                self.out1["pending_core_id"].append(d["pending_core_id"])
            else:
                print("erreur")
                exit()
        #plt.figure()
        #plt.plot(self.out0["delay"])
        #plt.show()
    def acces_history(self):   
        a = np.zeros(self.max_instr)   
        b = np.zeros(self.max_instr)   
        a[:len(self.list_acces_ddr0)] = self.list_acces_ddr0
        b[:len(self.list_acces_ddr1)] = self.list_acces_ddr1
        return a*b
    def addr_core(self,j):
        a = np.zeros(self.max_instr) - 1
        if j==0:
            a[:len(self.list_address0)] = self.list_address0
        elif j==1:
            a[:len(self.list_address1)] = self.list_address1
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
    instructions0 = make_random_list_instr(length=length, core=0)
    instructions1 = make_random_list_instr(length=length, core=1)
    return  {"core0": [instructions0],"core1":[instructions1]}

