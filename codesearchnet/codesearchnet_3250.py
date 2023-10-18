def SETPO(cpu, dest):
        """
        Sets byte if parity odd.

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        dest.write(Operators.ITEBV(dest.size, cpu.PF == False, 1, 0))