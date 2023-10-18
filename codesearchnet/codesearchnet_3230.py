def LEA(cpu, dest, src):
        """
        Loads effective address.

        Computes the effective address of the second operand (the source operand) and stores it in the first operand
        (destination operand). The source operand is a memory address (offset part) specified with one of the processors
        addressing modes; the destination operand is a general-purpose register. The address-size and operand-size
        attributes affect the action performed by this instruction. The operand-size
        attribute of the instruction is determined by the chosen register; the address-size attribute is determined by the
        attribute of the code segment.

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        dest.write(Operators.EXTRACT(src.address(), 0, dest.size))