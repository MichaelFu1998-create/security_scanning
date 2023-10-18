def RET(cpu, *operands):
        """
        Returns from procedure.

        Transfers program control to a return address located on the top of
        the stack. The address is usually placed on the stack by a CALL instruction,
        and the return is made to the instruction that follows the CALL instruction.
        The optional source operand specifies the number of stack bytes to be
        released after the return address is popped; the default is none.

        :param cpu: current CPU.
        :param operands: variable operands list.
        """
        # TODO FIX 64Bit FIX segment
        N = 0
        if len(operands) > 0:
            N = operands[0].read()
        cpu.PC = cpu.pop(cpu.address_bit_size)
        cpu.STACK += N