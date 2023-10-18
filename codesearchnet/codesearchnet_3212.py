def XADD(cpu, dest, src):
        """
        Exchanges and adds.

        Exchanges the first operand (destination operand) with the second operand
        (source operand), then loads the sum of the two values into the destination
        operand. The destination operand can be a register or a memory location;
        the source operand is a register.
        This instruction can be used with a LOCK prefix::

                TEMP  =  SRC + DEST
                SRC  =  DEST
                DEST  =  TEMP

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        MASK = (1 << dest.size) - 1
        SIGN_MASK = 1 << (dest.size - 1)

        arg0 = dest.read()
        arg1 = src.read()
        temp = (arg1 + arg0) & MASK
        src.write(arg0)
        dest.write(temp)

        # Affected flags: oszapc
        tempCF = Operators.OR(Operators.ULT(temp, arg0), Operators.ULT(temp, arg1))
        cpu.CF = tempCF
        cpu.AF = ((arg0 ^ arg1) ^ temp) & 0x10 != 0
        cpu.ZF = temp == 0
        cpu.SF = (temp & SIGN_MASK) != 0
        cpu.OF = (((arg0 ^ arg1 ^ SIGN_MASK) & (temp ^ arg1)) & SIGN_MASK) != 0
        cpu.PF = cpu._calculate_parity_flag(temp)