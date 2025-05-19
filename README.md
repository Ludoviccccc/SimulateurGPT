# curiosity-driven-approach

## On going:
I'm currenlty using `sim.class_mem_sim.py` to obtain the following informations:
* Quantifying contention. With the Interconnect.queue tool? ? 
* Link cause to effect of interference
* When do simultaneous accesses of an address from the L3 cache by both cores take place? ? 
* What other mechanisms are of interest to users/hardware engineers??
* What other mechanisms are responsible for interferences, and which only occur when two applications are run in parallel on both cores?
## Temporary choice ideas for IMGEP goal space: 
We want to identify a maximum of sources of interference, that is to say identify a maximum of scenarios where shared resources are used simultaneously by the two cores, here it can only be accessed by the two cores during the same cycle.
Below we show that it is simple to access a same address of the L3 cache during the same cycle:

```python
    instr0 = [{'type': 'r', 'addr': j, 'func': lambda val: None, 'core': 0} for j in range(20)]
    instr1 = [{'type': 'r', 'addr': j, 'func': lambda val: None, 'core': 1} for j in range(20)]
```
```
[L1 cache miss for 0 on core 1]
[L2 cache miss for 0 on core 1]
[L3 cache miss for 0 on core 1]
[Cycle 0] ➜ New CPU request queued: Core 1, READ Addr 0
[L1 cache miss for 0 on core 0]
[L2 cache miss for 0 on core 0]
[L3 cache miss for 0 on core 0]
[Cycle 0] ➜ New CPU request queued: Core 0, READ Addr 0
[Cycle 0] No pending DDR requests to schedule.
[L1 cache miss for 1 on core 1]
[L2 cache miss for 1 on core 1]
[L3 cache miss for 1 on core 1]
[Cycle 1] ➜ New CPU request queued: Core 1, READ Addr 1
[L1 cache miss for 1 on core 0]
[L2 cache miss for 1 on core 0]
[L3 cache miss for 1 on core 0]
[Cycle 1] ➜ New CPU request queued: Core 0, READ Addr 1
[Cycle 1] No pending DDR requests to schedule.
[L1 cache miss for 2 on core 1]
[L2 cache miss for 2 on core 1]
[L3 cache miss for 2 on core 1]
[Cycle 2] ➜ New CPU request queued: Core 1, READ Addr 2
[L1 cache miss for 2 on core 0]
[L2 cache miss for 2 on core 0]
[L3 cache miss for 2 on core 0]
[Cycle 2] ➜ New CPU request queued: Core 0, READ Addr 2
[Cycle 2] No pending DDR requests to schedule.
[L1 cache miss for 3 on core 1]
[L2 cache miss for 3 on core 1]
[L3 cache miss for 3 on core 1]
[Cycle 3] ➜ New CPU request queued: Core 1, READ Addr 3
[L1 cache miss for 3 on core 0]
[L2 cache miss for 3 on core 0]
[L3 cache miss for 3 on core 0]
[Cycle 3] ➜ New CPU request queued: Core 0, READ Addr 3
[Cycle 3] No pending DDR requests to schedule.
[L1 cache miss for 4 on core 1]
[L2 cache miss for 4 on core 1]
[L3 cache miss for 4 on core 1]
[Cycle 4] ➜ New CPU request queued: Core 1, READ Addr 4
[L1 cache miss for 4 on core 0]
[L2 cache miss for 4 on core 0]
[L3 cache miss for 4 on core 0]
[Cycle 4] ➜ New CPU request queued: Core 0, READ Addr 4
[Cycle 4] No pending DDR requests to schedule.
[L1 cache miss for 5 on core 1]
[L2 cache miss for 5 on core 1]
[L3 cache miss for 5 on core 1]
[Cycle 5] ➜ New CPU request queued: Core 1, READ Addr 5
[L1 cache miss for 5 on core 0]
[L2 cache miss for 5 on core 0]
[L3 cache miss for 5 on core 0]
[Cycle 5] ➜ New CPU request queued: Core 0, READ Addr 5
[Cycle 5] No pending DDR requests to schedule.
[L1 cache miss for 6 on core 1]
```

Mais supposons qu'il s'agit de quelque chose de pas si simple à faire.
Les listes d'instructions sont constituées d'instructions read and write. Il y'a un *cycle* par instruction.
Supposons les programmes consituées d'un nombre fixe de $n$ instructions.
### Idea 1

For parallel execution of a pair of programs: 
Matching a couple of vectors to constitute an objective: $(o_1, o_2) \in\{\{a_{0},...,a_{L}\}\cup\{-1\}\}^{n} \times \{\{a_{0},...,a_{L}\}\cup\{-1\}\}^{n}$  where $a_{\{0\leq i \leq L\}}$ are L3 memory addresses. coordinate equal to -1 corresponds to the fact that the cache L3 is not accessed.e.g $(o_1,o_2) = ((-1, -1, -1, a_{17}, -1, -1, a_{5}),(-1, a_{6}, a_{8}, -1, -1,-1, -1))$.

To construct a distance between two vector pairs $(u,v),(w, z)$, can be used a  **norm L1 or L2** *e.g* $d((a_1,a_2),(b_1, b_2)) = \sum_{i}^{n} |u_{i}-w_{i}| + \sum_{i}^{n} |v{i}-z_{i}| $, or the number of different coordinates between couples $d((u,v),(w, z)) = \sum_{i}^{n} (u_{i}==w_{i}) + (v_{i}==z_{i})$

 	Thus, an autothelial agent will want to browse a diversity of accesses on the L3 cache, situations where two cores access the same address and the same cycle may occur, which is a source of interference.

  However, this is not a useful way to use **IMGEP***, unless it is actually not easy to access the same address by two hearts, because you have to know in detail the architecture, moreover, you do not learn much, to my knowledge, except that it is possible to have an address of a shared cache line requested by both cores.
  
For an objective generator, I simply generate pairs of sequences with values in ${-1,0,...,19}$ to simulate 20 addresses on the L3 cache.

```python
class GoalGenerator:
    def __init__(self, max_len, num_addr):
        self.num_addr = num_addr
        self.max_len = max_len
    def __call__(self, epsilon = .3)->dict:
        def f():
            return np.random.randint(0, self.num_addr, (len_,))
        if np.random.binomial(1,1-epsilon):
            out = np.concatenate((f(),f()))
        else:
            instr = f()
            out = np.concatenate((instr, instr))
        return {"addr":out}
```

![Alt text](image/figure1.png)

![Alt text](image/figure2.png)

![Alt text](image/figure3.png)

### Idea 2	
For parallel execution of a pair of programs, match a vector of ${\{(1,0,0),(0,1,0), (0,0,1)\}}^{2n}$ with, during the cycle corresponding to the executed instruction:
	* (1,0,0) if the shared resource (L3) is accessed through reading. 
	* (0,1,0) if the shared resource is accessed for write.
	* (0,0,1) if the resource is not accessed.
	* There are $2n$ coordinates in the vector because we concatenate the information.
	* $\implies$ soliciting the shared resource 

## Description Simulateur Eric:
 This model represents a memory hierarchy with
 - 3 levels of cache (L1, L2, L3)
 - a DDR memory implemening some simple optimization features (see the DDR class)
 - an interconnect
 The number of cores, levels of cache, characteristics of the cache (number of ways,...)
 are parameters and can be modified.


* `mem_sim.CacheLine` represents a single cache line in the cache hierarchy

* `mem_sim.PLRU` Pseudo-LRU (PLRU) replacement policy for N-way set associative caches
The pseudoi-LRU is used to determine the bock to replace in case of cache miss.
A binary tree is used to implement the PLRU algorithm. here is one tree per set.

* `mem_sim.DDRRequest` represents a memory access request (either read or write)
* `mem_sim.Interconnect`: Interconnect model between CPU cores and DDR, with bandwidth and latency
* `mem_sim.DDRMemory`:  DDR memory model with banks, row buffers, and latency variations
