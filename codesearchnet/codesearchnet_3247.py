def SETO(cpu, dest):
        """
        Sets byte if overflow.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.OF, 1, 0))