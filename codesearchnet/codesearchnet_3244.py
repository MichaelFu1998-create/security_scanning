def SETNO(cpu, dest):
        """
        Sets byte if not overflow.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.OF == False, 1, 0))