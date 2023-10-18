def XOR(cpu, dest, src):
        """
        Logical exclusive OR.

        Performs a bitwise exclusive Operators.OR(XOR) operation on the destination (first)
        and source (second) operands and stores the result in the destination
        operand location.

        Each bit of the result is 1 if the corresponding bits of the operands
        are different; each bit is 0 if the corresponding bits are the same.

        The OF and CF flags are cleared; the SF, ZF, and PF flags are set according to the result::

            DEST  =  DEST XOR SRC;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        if dest == src:
            # if the operands are the same write zero
            res = dest.write(0)
        else:
            res = dest.write(dest.read() ^ src.read())
        # Defined Flags: szp
        cpu._calculate_logic_flags(dest.size, res)