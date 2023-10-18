def XCHG(cpu, dest, src):
        """
        Exchanges register/memory with register.

        Exchanges the contents of the destination (first) and source (second)
        operands. The operands can be two general-purpose registers or a register
        and a memory location. If a memory operand is referenced, the processor's
        locking protocol is automatically implemented for the duration of the
        exchange operation, regardless of the presence or absence of the LOCK
        prefix or of the value of the IOPL.
        This instruction is useful for implementing semaphores or similar data
        structures for process synchronization.
        The XCHG instruction can also be used instead of the BSWAP instruction
        for 16-bit operands::

                TEMP  =  DEST
                DEST  =  SRC
                SRC  =  TEMP

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        temp = dest.read()
        dest.write(src.read())
        src.write(temp)