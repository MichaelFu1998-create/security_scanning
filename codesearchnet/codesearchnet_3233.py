def SETA(cpu, dest):
        """
        Sets byte if above.

        Sets the destination operand to 0 or 1 depending on the settings of the status flags (CF, SF, OF, ZF, and PF, 1, 0) in the
        EFLAGS register. The destination operand points to a byte register or a byte in memory. The condition code suffix
        (cc, 1, 0) indicates the condition being tested for::
                IF condition
                THEN
                    DEST = 1;
                ELSE
                    DEST = 0;
                FI;

        :param cpu: current CPU.
        :param dest: destination operand.
         """
        dest.write(Operators.ITEBV(dest.size, Operators.OR(cpu.CF, cpu.ZF) == False, 1, 0))