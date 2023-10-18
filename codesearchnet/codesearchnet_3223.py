def CMOVGE(cpu, dest, src):
        """
        Conditional move - Greater or equal/not less.

        Tests the status flags in the EFLAGS register and moves the source operand
        (second operand) to the destination operand (first operand) if the given
        test condition is true.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        dest.write(Operators.ITEBV(dest.size, (cpu.SF ^ cpu.OF) == 0, src.read(), dest.read()))