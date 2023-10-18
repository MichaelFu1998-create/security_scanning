def SETE(cpu, dest):
        """
        Sets byte if equal.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.ZF, 1, 0))