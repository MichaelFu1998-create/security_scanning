def PSRLDQ(cpu, dest, src):
        """
        Packed shift right logical double quadword.

        Shifts the destination operand (first operand) to the right by the number
        of bytes specified in the count operand (second operand). The empty high-order
        bytes are cleared (set to all 0s). If the value specified by the count
        operand is greater than 15, the destination operand is set to all 0s.
        The destination operand is an XMM register. The count operand is an 8-bit
        immediate::

            TEMP  =  SRC;
            if (TEMP > 15) TEMP  =  16;
            DEST  =  DEST >> (temp * 8);

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: count operand.
        """
        # TODO(yan): Verify the correctness of truncating SRC like this ( tests
        # use '-1' as the value
        temp = Operators.EXTRACT(src.read(), 0, 8)
        temp = Operators.ITEBV(src.size, temp > 15, 16, temp)
        dest.write(dest.read() >> (temp * 8))