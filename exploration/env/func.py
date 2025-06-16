from sim.sim_use import runpgrms, make_random_list_instr, make_random_paire_list_instr
from sim.ddr import DDRMemory
from sim.class_mem_sim import *
from sim.sim_use import runpgrms, make_random_list_instr


class Env:
    def __init__(self,
                l1_conf = {'size': 32,  'line_size': 4, 'assoc': 2},
                l2_conf = {'size': 128, 'line_size': 4, 'assoc': 4},
                l3_conf = {'size': 512, 'line_size': 4, 'assoc': 8},
                ):
        self.l1_conf = l1_conf
        self.l2_conf = l2_conf
        self.l3_conf = l3_conf
        self.repetition = 5
        #self.max_len = max_len
        #self.length_programs = length_programs
    def __call__(self, parameter:dict)->dict:
        program = self._make_program()
        program0 = self._make_program()
        program1 = self._make_program()
        program(parameter["core0"][0], parameter["core1"][0])
        program0(parameter["core0"][0],[])
        program1([],parameter["core1"][0])
        return {
                "miss_ratios": program.ratios,
                "miss_ratios_core0": program0.ratios,
                "miss_ratios_core1": program1.ratios,
                "time_core0_together":program.compl_time_core0,
                "time_core1_together":program.compl_time_core1,
                "time_core0_alone":program0.compl_time_core0,
                "time_core1_alone":program1.compl_time_core1,
                "miss_count":program.miss_count,
                "miss_count_core0":program0.miss_count,
                "miss_count_core1":program1.miss_count,
                "diff_ratios_core0":np.abs(program.ratios - program0.ratios),
                "diff_ratios_core1":np.abs(program.ratios - program1.ratios),
                "diff_time0":np.abs(program.compl_time_core0 - program0.compl_time_core0),
                "diff_time1":np.abs(program.compl_time_core1 - program1.compl_time_core1)
                }
    def call2(self, parameter:dict)->dict:
        program = [self._make_program() for j in range(self.repetition)]
        program0 = [self._make_program() for j in range(self.repetition)]
        program1 = [self._make_program() for j in range(self.repetition)]
        for j in range(self.repetition):
            program[j](parameter["core0"][0], parameter["core1"][0])
            program0[j](parameter["core0"][0],[])
            program1[j]([],parameter["core1"][0])
        return {
                "miss_ratios": np.mean([program[j].ratios for j in range(self.repetition)],axis=0),
                "miss_ratios_core0": np.mean([program0[j].ratios for j in range(self.repetition)],axis=0),
                "miss_ratios_core1": np.mean([program1[j].ratios for j in range(self.repetition)],axis=0),
                "time_core0_together":np.mean([program[j].compl_time_core0 for j in range(self.repetition)],axis=0),
                "time_core1_together":np.mean([program[j].compl_time_core1],axis=0),
                "time_core0_alone":np.mean([program0[j].compl_time_core0],axis=0),
                "time_core1_alone":np.mean([program1[j].compl_time_core1],axis=0),
                "miss_count":np.mean([program[j].miss_count],axis=0),
                "miss_count_core0":np.mean([program0[j].miss_count],axis=0),
                "miss_count_core1":np.mean([program1[j].miss_count],axis=0),
                "diff_ratios_core0":np.mean([np.abs(program[j].ratios - program0[j].ratios)],axis=0),
                "diff_ratios_core1":np.mean([np.abs(program[j].ratios - program1[j].ratios)],axis=0),
                "diff_time0":np.mean([np.abs(program[j].compl_time_core0 - program0[j].compl_time_core0)],axis=0),
                "diff_time1":np.mean([np.abs(program[j].compl_time_core1 - program1[j].compl_time_core1)],axis=0),

                "miss_ratios_detailled": np.mean([program[j].ratios_tab for j in range(self.repetition)],axis=0),
                "miss_ratios_core0_detailled": np.mean([program0[j].ratios_tab for j in range(self.repetition)],axis=0),
                "miss_ratios_core1_detailled": np.mean([program1[j].ratios_tab for j in range(self.repetition)],axis=0),

                }
    def _make_program(self):
        ddr = DDRMemory()
        interconnect = Interconnect(ddr, delay=5, bandwidth=4)
        core0 = MultiLevelCache(0, self.l1_conf, self.l2_conf, self.l3_conf, interconnect)
        core1 = MultiLevelCache(1, self.l1_conf, self.l2_conf, self.l3_conf, interconnect)
        return runpgrms(core0, core1, interconnect, ddr)
