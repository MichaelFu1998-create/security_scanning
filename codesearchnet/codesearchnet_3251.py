def SETS(cpu, dest):
        """
        Sets byte if sign.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.SF, 1, 0))