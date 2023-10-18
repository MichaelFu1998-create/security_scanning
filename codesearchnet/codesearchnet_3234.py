def SETB(cpu, dest):
        """
        Sets byte if below.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.CF, 1, 0))