def SETBE(cpu, dest):
        """
        Sets byte if below or equal.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, Operators.OR(cpu.CF, cpu.ZF), 1, 0))