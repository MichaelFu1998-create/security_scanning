def NEG(cpu, dest):
        """
        Two's complement negation.

        Replaces the value of operand (the destination operand) with its two's complement.
        (This operation is equivalent to subtracting the operand from 0.) The destination operand is
        located in a general-purpose register or a memory location::

                IF DEST  =  0
                THEN CF  =  0
                ELSE CF  =  1;
                FI;
                DEST  =  - (DEST)

        :param cpu: current CPU.
        :param dest: destination operand.
        """
        source = dest.read()
        res = dest.write(-source)
        cpu._calculate_logic_flags(dest.size, res)
        cpu.CF = source != 0
        cpu.AF = (res & 0x0f) != 0x00