# curiosity-driven-approach

## En cours:
Utiliser `sim.class_mem_sim.py` pour obtenir les informations suivantes:
* Quantifier la contention. Avec l'attribu Interconnect.queue ? 
* Faire lien cause à effet d'interférences
* Quand ont lieu les accès simultanés d'une adresse du cache L3 par les deux coeurs ? 
* Quels autres mécanismes sont d'interet pour des utilisateurs/ingénieur hardware?
* Quels autres mécanismes sont responsables des inteférences, et qui ne se produisent **uniquement** lorsque deux applications sont exécutées en parallèle sur les deux coeurs?
## Idées de choix temporaires pour espace des objectifs IMGEP: 
La méthode vise à explorer au mieux un système complexe, pour lequel il est difficile de connaitre tous les comportements où états dans lesquels il me se trouver, en manipulant ses paramètres au hasard ou avec des stratégies prédéfinies.
On souhaite identifier un maximum de sources d'interférences, c'est à dire identifier un maximum de scénarios où des ressources partagées sont utilisées simulatément par les deux coeurs, ici il ne peut s'agir que d''adresses accedées par les deux coeurs pendant le meme cycle.
Ci-dessous on montre qu'il est simple d'acceder à une meme adresse du cache L3 pendant le meme cycle:
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
### Idée 1
Pour l'exécution parallèle d'une paire de programmes:
 Faire correspondre un couple de vecteurs pour consistituer un objectif: $(o_1, o_2) \in\{\{a_{0},...,a_{L}\}\cup\{-1\}\}^{n}\times \{\{a_{0},...,a_{L}\}\cup\{-1\}\}^{n}$  où $L$ est le nombre d'adresses du cache L3, les $a_{\{0\leq i \leq L\}}$ sont les adresses mémoires du cache partagé L3. Une coordonée égale à -1 correspond au fait que le cache L3 n'est pas accedé. e.g $(o_1,o_2)\in((-1, -1, -1, a_{17}, -1, -1, a_{5}),(-1, a_{6}, a_{8}, -1, -1,-1, -1))$.
 Pour constituer une distance entre deux couples de vecteurs $(u,v),(w, z)$ 
, on peut utiliser une **norme L1 ou L2** *e.g* $d((a_1,a_2),(b_1, b_2)) = \sum_{i}^{n} |u_{i}-w_{i}| + \sum_{i}^{n} |v{i}-z_{i}| $, ou **le nombre de coordonnées différentes entre les couples**  $$d((u,v),(w, z)) = \sum_{i}^{n} \mathbb{1}_{\{u_i=w_i\}} + \sum_{i}^{n} \mathbb{1}_{\{v_i=z_i\}}$$. 
	Ainsi, un agent autothélique souhaitera parcourir une diversité d'accès sur le cache L3, des situations où deux coeurs accèdent à la meme adresse et au meme cycle pourront se produire, ce qui correpond à une source d'interférence. Cependant ce n'est pas une façon utile d'utiliser **IMGEP**, sauf s'il n'est en réalité pas facile d'acceder à la meme adresse par deux coeurs, car il faut connaitre en détail l'architecture, de plus, on n'apprend pas grand chose, à ma connaissance, à part qu'il est possible d'avoir une adresse d'une ligne de cache partagée sollicitée par les deux coeurs.

Pour un generateur d'objectif, je génère simplement des paires de séquences à valeurs dans ${0,...,19}$ pour simuler 20 adresses sur le cache L3.

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

### Idée 2	

Pour l'exécution parallèle d'une paire de programmes, faire correspondre un vecteur de ${\{(1,0,0),(0,1,0), (0,0,1)\}}^{2n}$ avec, lors du cycle correspondant à l'instruction exécutée:
	* (1,0,0) si la ressource partagée (L3) est accedée enlecture. 
	* (0,1,0) si la ressource partagée est accedée en écriture.
	* (0,0,1) si la ressource n'est pas accedée.
	* Il y a $2n$ coordonnées dans le vecteur car on concatène les informations.
	* $\implies$ solliciter la ressource partagée 
	* Ellaboration d'une distance

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
