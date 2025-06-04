from sim.sim_use import runpgrms, make_random_list_instr, make_random_paire_list_instr
from sim.ddr import DDRMemory
from sim.class_mem_sim import *
from sim.sim_use import runpgrms, make_random_list_instr


class Env:
    def __init__(self,
                l1_conf = {'size': 32,  'line_size': 4, 'assoc': 2},
                l2_conf = {'size': 128, 'line_size': 4, 'assoc': 4},
                l3_conf = {'size': 512, 'line_size': 4, 'assoc': 8},
                length_programs = 50,
                max_len=350):
        self.l1_conf = l1_conf
        self.l2_conf = l2_conf
        self.l3_conf = l3_conf
        self.max_len = max_len
        self.length_programs = length_programs
    def __call__(self, parameter:dict):
        program = self._make_program()
        program0 = self._make_program()
        program1 = self._make_program()
        program(parameter["core0"][0], parameter["core1"][0])
        program0(parameter["core0"][0],[])
        program1([],parameter["core1"][0])
        return {"core0":program.out0,
                "core1":program.out1,
                "core0_alone":program0.out0,
                "core1_alone":program1.out1,
                "perf": program.ratios,
                "perf_core0": program0.ratios,
                "perf_core1": program1.ratios,
                "time_core0_together":program.compl_time_core0,
                "time_core1_together":program.compl_time_core1,
                "time_core0_alone":program0.compl_time_core0,
                "time_core1_alone":program1.compl_time_core1,
                }
    def _make_program(self):
        ddr = DDRMemory()
        interconnect = Interconnect(ddr, delay=5, bandwidth=4)
        core0 = MultiLevelCache(0, self.l1_conf, self.l2_conf, self.l3_conf, interconnect)
        core1 = MultiLevelCache(1, self.l1_conf, self.l2_conf, self.l3_conf, interconnect)
        return runpgrms(core0, core1, self.length_programs, interconnect, ddr, max_len=self.max_len)
