def AND(cpu, dest, src):
        """
        Logical AND.

        Performs a bitwise AND operation on the destination (first) and source
        (second) operands and stores the result in the destination operand location.
        Each bit of the result is set to 1 if both corresponding bits of the first and
        second operands are 1; otherwise, it is set to 0.

        The OF and CF flags are cleared; the SF, ZF, and PF flags are set according to the result::

            DEST  =  DEST AND SRC;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        # XXX bypass a capstone bug that incorrectly extends and computes operands sizes
        # the bug has been fixed since capstone 4.0.alpha2 (commit de8dd26)
        if src.size == 64 and src.type == 'immediate' and dest.size == 64:
            arg1 = Operators.SEXTEND(src.read(), 32, 64)
        else:
            arg1 = src.read()
        res = dest.write(dest.read() & arg1)
        # Defined Flags: szp
        cpu._calculate_logic_flags(dest.size, res)