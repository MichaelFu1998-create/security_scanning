def MOVQ(cpu, dest, src):
        """
        Move quadword.

        Copies a quadword from the source operand (second operand) to the destination operand (first operand).
        The source and destination operands can be MMX(TM) technology registers, XMM registers, or 64-bit memory
        locations. This instruction can be used to move a between two MMX registers or between an MMX register
        and a 64-bit memory location, or to move data between two XMM registers or between an XMM register and
        a 64-bit memory location. The instruction cannot be used to transfer data between memory locations.
        When the source operand is an XMM register, the low quadword is moved; when the destination operand is
        an XMM register, the quadword is stored to the low quadword of the register, and the high quadword is
        cleared to all 0s::

            MOVQ instruction when operating on MMX registers and memory locations:

            DEST  =  SRC;

            MOVQ instruction when source and destination operands are XMM registers:

            DEST[63-0]  =  SRC[63-0];

            MOVQ instruction when source operand is XMM register and destination operand is memory location:

            DEST  =  SRC[63-0];

            MOVQ instruction when source operand is memory location and destination operand is XMM register:

            DEST[63-0]  =  SRC;
            DEST[127-64]  =  0000000000000000H;

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        # mmx to mmx or mmx to mem
        if dest.size == src.size and dest.size == 64:
            dest.write(src.read())
        # two xmm regs
        elif dest.size == src.size and dest.size == 128:
            src_lo = Operators.EXTRACT(src.read(), 0, 64)
            dest.write(Operators.ZEXTEND(src_lo, 128))
        # mem to xmm
        elif dest.size == 128 and src.size == 64:
            dest.write(Operators.ZEXTEND(src.read(), dest.size))
        # xmm to mem
        elif dest.size == 64 and src.size == 128:
            dest.write(Operators.EXTRACT(src.read(), 0, dest.size))
        else:
            msg = 'Invalid size in MOVQ'
            logger.error(msg)
            raise Exception(msg)