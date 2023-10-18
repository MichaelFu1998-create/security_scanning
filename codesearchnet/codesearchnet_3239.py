def SETNAE(cpu, dest):
        """
        Sets byte if not above or equal.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.CF, 1, 0))