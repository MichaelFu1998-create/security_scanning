def PXOR(cpu, dest, src):
        """
        Logical exclusive OR.

        Performs a bitwise logical exclusive-OR (XOR) operation on the quadword
        source (second) and destination (first) operands and stores the result
        in the destination operand location. The source operand can be an MMX(TM)
        technology register or a quadword memory location; the destination operand
        must be an MMX register. Each bit of the result is 1 if the corresponding
        bits of the two operands are different; each bit is 0 if the corresponding
        bits of the operands are the same::

            DEST  =  DEST XOR SRC;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: quadword source operand.
        """
        res = dest.write(dest.read() ^ src.read())