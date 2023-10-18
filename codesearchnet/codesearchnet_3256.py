def POPF(cpu):
        """
        Pops stack into EFLAGS register.

        :param cpu: current CPU.
        """
        mask = (0x00000001 |
                0x00000004 |
                0x00000010 |
                0x00000040 |
                0x00000080 |
                0x00000400 |
                0x00000800)
        val = cpu.pop(16)
        eflags_size = 32
        cpu.EFLAGS = Operators.ZEXTEND(val & mask, eflags_size)