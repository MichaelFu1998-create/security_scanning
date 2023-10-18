def SETNB(cpu, dest):
        """
        Sets byte if not below.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.CF == False, 1, 0))