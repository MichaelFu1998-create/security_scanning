def POPFQ(cpu):
        """
        Pops stack into EFLAGS register.

        :param cpu: current CPU.
        """
        mask = 0x00000001 | 0x00000004 | 0x00000010 | 0x00000040 | 0x00000080 | 0x00000400 | 0x00000800
        cpu.EFLAGS = (cpu.EFLAGS & ~mask) | cpu.pop(64) & mask