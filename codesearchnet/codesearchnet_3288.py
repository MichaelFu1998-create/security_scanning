def SHR(cpu, dest, src):
        """
        Shift logical right.

        The shift arithmetic right (SAR) and shift logical right (SHR)
        instructions shift the bits of the destination operand to the right
        (toward less significant bit locations). For each shift count, the
        least significant bit of the destination operand is shifted into the CF
        flag, and the most significant bit is either set or cleared depending
        on the instruction type. The SHR instruction clears the most
        significant bit.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: count operand.
        """
        OperandSize = dest.size
        count = Operators.ZEXTEND(src.read() & (OperandSize - 1), OperandSize)
        value = dest.read()

        res = dest.write(value >> count)  # UNSIGNED Operators.UDIV2 !! TODO Check

        MASK = (1 << OperandSize) - 1
        SIGN_MASK = 1 << (OperandSize - 1)

        if issymbolic(count):
            cpu.CF = Operators.ITE(count != 0,
                                   ((value >> Operators.ZEXTEND(count - 1, OperandSize)) & 1) != 0,
                                   cpu.CF)
        else:
            if count != 0:
                cpu.CF = Operators.EXTRACT(value, count - 1, 1) != 0

        cpu.ZF = Operators.ITE(count != 0, res == 0, cpu.ZF)
        cpu.SF = Operators.ITE(count != 0, (res & SIGN_MASK) != 0, cpu.SF)
        # OF is only defined for count == 1, but in practice (unit tests from real cpu) it's calculated for count != 0
        cpu.OF = Operators.ITE(count != 0, ((value >> (OperandSize - 1)) & 0x1) == 1, cpu.OF)
        cpu.PF = Operators.ITE(count != 0, cpu._calculate_parity_flag(res), cpu.PF)