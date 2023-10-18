def SETNZ(cpu, dest):
        """
        Sets byte if not zero.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.ZF == False, 1, 0))