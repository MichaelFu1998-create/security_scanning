def RDTSC(cpu):
        """
        Reads time-stamp counter.

        Loads the current value of the processor's time-stamp counter into the
        EDX:EAX registers.  The time-stamp counter is contained in a 64-bit
        MSR. The high-order 32 bits of the MSR are loaded into the EDX
        register, and the low-order 32 bits are loaded into the EAX register.
        The processor increments the time-stamp counter MSR every clock cycle
        and resets it to 0 whenever the processor is reset.

        :param cpu: current CPU.
        """
        val = cpu.icount
        cpu.RAX = val & 0xffffffff
        cpu.RDX = (val >> 32) & 0xffffffff