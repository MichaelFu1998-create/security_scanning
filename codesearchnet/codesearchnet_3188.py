def CPUID(cpu):
        """
        CPUID instruction.

        The ID flag (bit 21) in the EFLAGS register indicates support for the
        CPUID instruction.  If a software procedure can set and clear this
        flag, the processor executing the procedure supports the CPUID
        instruction. This instruction operates the same in non-64-bit modes and
        64-bit mode.  CPUID returns processor identification and feature
        information in the EAX, EBX, ECX, and EDX registers.

        The instruction's output is dependent on the contents of the EAX
        register upon execution.

        :param cpu: current CPU.
        """
        # FIXME Choose conservative values and consider returning some default when eax not here
        conf = {0x0: (0x0000000d, 0x756e6547, 0x6c65746e, 0x49656e69),
                0x1: (0x000306c3, 0x05100800, 0x7ffafbff, 0xbfebfbff),
                0x2: (0x76035a01, 0x00f0b5ff, 0x00000000, 0x00c10000),
                0x4: {0x0: (0x1c004121, 0x01c0003f, 0x0000003f, 0x00000000),
                      0x1: (0x1c004122, 0x01c0003f, 0x0000003f, 0x00000000),
                      0x2: (0x1c004143, 0x01c0003f, 0x000001ff, 0x00000000),
                      0x3: (0x1c03c163, 0x03c0003f, 0x00000fff, 0x00000006)},
                0x7: (0x00000000, 0x00000000, 0x00000000, 0x00000000),
                0x8: (0x00000000, 0x00000000, 0x00000000, 0x00000000),
                0xb: {0x0: (0x00000001, 0x00000002, 0x00000100, 0x00000005),
                      0x1: (0x00000004, 0x00000004, 0x00000201, 0x00000003)},
                0xd: {0x0: (0x00000000, 0x00000000, 0x00000000, 0x00000000),
                      0x1: (0x00000000, 0x00000000, 0x00000000, 0x00000000)},
                }

        if cpu.EAX not in conf:
            logger.warning('CPUID with EAX=%x not implemented @ %x', cpu.EAX, cpu.PC)
            cpu.EAX, cpu.EBX, cpu.ECX, cpu.EDX = 0, 0, 0, 0
            return

        if isinstance(conf[cpu.EAX], tuple):
            cpu.EAX, cpu.EBX, cpu.ECX, cpu.EDX = conf[cpu.EAX]
            return

        if cpu.ECX not in conf[cpu.EAX]:
            logger.warning('CPUID with EAX=%x ECX=%x not implemented', cpu.EAX, cpu.ECX)
            cpu.EAX, cpu.EBX, cpu.ECX, cpu.EDX = 0, 0, 0, 0
            return

        cpu.EAX, cpu.EBX, cpu.ECX, cpu.EDX = conf[cpu.EAX][cpu.ECX]