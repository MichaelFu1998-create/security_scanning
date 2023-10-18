def SAR(cpu, dest, src):
        """
        Shift arithmetic right.

        The shift arithmetic right (SAR) and shift logical right (SHR) instructions shift the bits of the destination operand to
        the right (toward less significant bit locations). For each shift count, the least significant bit of the destination
        operand is shifted into the CF flag, and the most significant bit is either set or cleared depending on the instruction
        type. The SHR instruction clears the most significant bit. the SAR instruction sets or clears the most significant bit
        to correspond to the sign (most significant bit) of the original value in the destination operand. In effect, the SAR
        instruction fills the empty bit position's shifted value with the sign of the unshifted value

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        OperandSize = dest.size
        countMask = {8: 0x1f,
                     16: 0x1f,
                     32: 0x1f,
                     64: 0x3f}[OperandSize]

        count = src.read() & countMask
        value = dest.read()

        res = Operators.SAR(OperandSize, value, Operators.ZEXTEND(count, OperandSize))
        dest.write(res)

        SIGN_MASK = (1 << (OperandSize - 1))

        # We can't use this one as the 'true' expression gets eagerly calculated even on count == 0		 +        cpu.CF = Operators.ITE(count!=0, ((value >> Operators.ZEXTEND(count-1, OperandSize)) & 1) !=0, cpu.CF)
        # cpu.CF = Operators.ITE(count!=0, ((value >> Operators.ZEXTEND(count-1, OperandSize)) & 1) !=0, cpu.CF)

        if issymbolic(count):
            # We can't use this one as the EXTRACT op needs the offset arguments to be concrete
            #    cpu.CF = Operators.ITE(count!=0, Operands.EXTRACT(value,count-1,1) !=0, cpu.CF)
            cpu.CF = Operators.ITE(Operators.AND(count != 0, count <= OperandSize), ((value >> Operators.ZEXTEND(count - 1, OperandSize)) & 1) != 0, cpu.CF)
        else:
            if count != 0:
                if count > OperandSize:
                    count = OperandSize
                cpu.CF = Operators.EXTRACT(value, count - 1, 1) != 0

        # on count == 0 AF is unaffected, for count > 0, AF is undefined.
        # in either case, do not touch AF
        cpu.ZF = Operators.ITE(count != 0, res == 0, cpu.ZF)
        cpu.SF = Operators.ITE(count != 0, (res & SIGN_MASK) != 0, cpu.SF)
        cpu.OF = Operators.ITE(count == 1, False, cpu.OF)
        cpu.PF = Operators.ITE(count != 0, cpu._calculate_parity_flag(res), cpu.PF)