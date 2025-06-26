Eric Jenn from (research engineer from Saint-Exupéry) also made a simulator with GPT. As an expert, Eric has obviously been able to write better prompts to get a more detailed simulator.
It is a dual core hardware with two private cache L1 and L2 (i.e each core has private memory) and a main memory L3. An interconnect (bus) is modeled (not with actual details). 
## Interconnect
To transfer commands, addresses and written and read data, to interconnects are used. Here is a simple model is implemented. Each request takes at least some base delay to be served (ie. based delay + random, ), while being pushed in a **request queue**then its **ready_time** is fixed.  A request may be delayed if the **interconnect bandwidh** has been "used".
At each **cycle**, the received instructions received from the cache are sent to the **DDR** accordingly to their **readu_time** and the current cycle.
This model allows to model `bus contention`.
## Cache Structure:
Each level of cache is organized as an array containing data. `Blocks` are columns, and `lines` is also a crucial notion.
```
Set 0: [Block 0] [Block 1] [Block 2] [Block 3]  ← 4-way associativity (n=4)
Set 1: [Block 0] [Block 1] [Block 2] [Block 3]
...
Set N: [Block 0] [Block 1] [Block 2] [Block 3]
```

The simulator reads a minimal set of assembly instructions (read and write). e.g
` instr0 = {'type': 'r', 'addr': 4, 'func': lambda val: None, 'core': 0}`
`instr1 = {'type': 'w', 'addr': 4, 'value': l42, 'core': 0} `.

A cache-address can be broken up up in 3 parts. 
+----------------+-----------+-----------+
 |     Tag        |   Index   |  Offset   |
+----------------+-----------+-----------+

    the offset within the block
    the index that identifies the set
    the tag that identifies the block in the set.

When a request comes in, the index is calculated to identify the set. Then the tags of all blocks in the set are checked. And when a block with a matching tag is found, if this is a **read request**, the right bytes are returned based on the offset, then a `cache hit` occurs. If this is a **write request** and the line (where we want to write) is avaible then this is also a `cache hit`.

    • Cache Hit: When the requested data is found directly in the cache : fast access, no need to go to main memory.
    • Cache Miss: When the data is not found in the cache : the system must fetch it from **slower memory** (lower cache or DDR), which increases latency.

## DDR Structure or main memory

DDR has a larger storage capacity but the time to acces data is longer (10-100 longer) than cache.
I am still figuring out how this implementation works. Here is what I understand so far:
In general DDRAM is made of a set of modules that communicates with interconnects (several bus). a module is made of several chips that are gathered in ranks(see image). These chips are made of several **banks**. A bank is basically a matrix of lines called **rows**. An additional row is called **rwo buffer**. 
A row buffer holds read data.  Whenever a data is accessed, the content of the corresponding line is loaded in the row buffer. This handles the fact that reading a line erases its content! It also reduces the acces time to this data.
* There is a **row miss** If data from the line we want to the read or write is not loaded in the *row buffer*. The data still needs to be loaded in the buffer reading it and thus a delay is needed.

Acces latencies depend on the active bank. Each bank has a row buffer.
When read and write instructions are performed at cache level, requests are sent to ddr, and stored in a queue, sorted accordingly to differents criteria,i.e accesses to busy banks are avoided, row hits are prefered.

This implementation allows to model `memory contention` (When multiple cores access a shared memory simultaneously in the same bank leading to a bottleneck due to limited memory bandwidth).


## What I do now
* Selection of observations to characterize interferences, not necessarly to constitute the objective space of IMGEP!
* Visualisation of random exploration: I seek to vizualize the selected observations characterizing interference phenomena  in a way that shows diversity.
* Toulouse people want me to implement IMGEP with some micro-architectural behaviors constituting the objective space --> I think could be better to have info on delay as a objective space and see after what micro-architectural components are involved. This would lead to a more adaptable tool, because having  micro-architectural behaviors constituting requires both knowledge of the architecture and and data science knowledge.
* Toulouse people want me to implement IMGEP with some micro-architectural behaviors constituting the objective space.  
* To actually show what I do : link github: https://github.com/Ludoviccccc/SimulateurGPT
