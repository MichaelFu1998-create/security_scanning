def CMOVA(cpu, dest, src):
        """
        Conditional move - Above/not below or equal.

        Tests the status flags in the EFLAGS register and moves the source operand
        (second operand) to the destination operand (first operand) if the given
        test condition is true.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        dest.write(Operators.ITEBV(dest.size, Operators.AND(cpu.CF == False, cpu.ZF == False), src.read(), dest.read()))