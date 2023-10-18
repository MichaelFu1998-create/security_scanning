def PSLLDQ(cpu, dest, src):
        """ Packed Shift Left Logical Double Quadword
        Shifts the destination operand (first operand) to the left by the number
         of bytes specified in the count operand (second operand). The empty low-order
         bytes are cleared (set to all 0s). If the value specified by the count
         operand is greater than 15, the destination operand is set to all 0s.
         The destination operand is an XMM register. The count operand is an 8-bit
         immediate.

            TEMP  =  COUNT;
            if (TEMP > 15) TEMP  =  16;
            DEST  =  DEST << (TEMP * 8);
        """
        count = Operators.ZEXTEND(src.read(), dest.size * 2)
        byte_count = Operators.ITEBV(src.size * 2, count > 15, 16, count)
        bit_count = byte_count * 8
        val = Operators.ZEXTEND(dest.read(), dest.size * 2)
        val = val << (Operators.ZEXTEND(bit_count, dest.size * 2))
        dest.write(Operators.EXTRACT(val, 0, dest.size))