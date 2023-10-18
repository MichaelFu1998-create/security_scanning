def SETNBE(cpu, dest):
        """
        Sets byte if not below or equal.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, Operators.AND(cpu.CF == False, cpu.ZF == False), 1, 0))