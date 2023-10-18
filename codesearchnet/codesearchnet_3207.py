def INC(cpu, dest):
        """
        Increments by 1.

        Adds 1 to the destination operand, while preserving the state of the
        CF flag. The destination operand can be a register or a memory location.
        This instruction allows a loop counter to be updated without disturbing
        the CF flag. (Use a ADD instruction with an immediate operand of 1 to
        perform an increment operation that does updates the CF flag.)::

                DEST  =  DEST +1;

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        arg0 = dest.read()
        res = dest.write(arg0 + 1)
        res &= (1 << dest.size) - 1
        SIGN_MASK = 1 << (dest.size - 1)
        cpu.AF = ((arg0 ^ 1) ^ res) & 0x10 != 0
        cpu.ZF = res == 0
        cpu.SF = (res & SIGN_MASK) != 0
        cpu.OF = res == SIGN_MASK
        cpu.PF = cpu._calculate_parity_flag(res)