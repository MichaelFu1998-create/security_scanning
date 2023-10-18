def SETP(cpu, dest):
        """
        Sets byte if parity.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.PF, 1, 0))