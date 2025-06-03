import random
import time
import numpy as np
from exploration.random.func import RANDOM
from exploration.env.func import Env
from exploration.history import History
from exploration.imgep.goal_generator import GoalGenerator2
from exploration.imgep.OptimizationPolicy import OptimizationPolicykNN
from exploration.imgep.imgep import IMGEP
import matplotlib.pyplot as plt
from visu import representation, comparaison

if __name__=="__main__":
    random.seed(0)
    N = int(200)
    N_init = 50
    max_len = 500  
    length_programs = 100

    H_rand = History(max_size=1000)
    H2_rand = History(max_size=1000)
    En = Env(length_programs=length_programs, max_len=max_len)
    rand = RANDOM(N = N,E = En, H = H_rand, H2 = H2_rand)
    rand()
    content_random = H_rand.present_content()
    print("content_random", content_random.keys())
    print("content_random", min(content_random["time_core0_together"]), max(content_random["time_core0_together"]))
    print("content_random", min(content_random["time_core1_together"]), max(content_random["time_core1_together"]))
    
    G = GoalGenerator2(max_len = 0,num_addr = 10)
    Pi = OptimizationPolicykNN(k=10,mutation_rate=.1,max_len=50)
    H_imgep = History(max_size=1000)
    H2_imgep = History(max_size=1000)

    imgep = IMGEP(N,N_init, En,H_imgep,G,Pi)
    imgep()
    content_imgep = H_imgep.present_content()
    #representation(content_imgep)
    comparaison(content_random, content_imgep)
