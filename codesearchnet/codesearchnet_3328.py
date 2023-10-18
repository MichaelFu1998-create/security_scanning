def MOVSS(cpu, dest, src):
        """
        Moves a scalar single-precision floating-point value

        Moves a scalar single-precision floating-point value from the source operand (second operand)
        to the destination operand (first operand). The source and destination operands can be XMM
        registers or 32-bit memory locations. This instruction can be used to move a single-precision
        floating-point value to and from the low doubleword of an XMM register and a 32-bit memory
        location, or to move a single-precision floating-point value between the low doublewords of
        two XMM registers. The instruction cannot be used to transfer data between memory locations.
        When the source and destination operands are XMM registers, the three high-order doublewords of the
        destination operand remain unchanged. When the source operand is a memory location and destination
        operand is an XMM registers, the three high-order doublewords of the destination operand are cleared to all 0s.

        //MOVSS instruction when source and destination operands are XMM registers:
        if(IsXMM(Source) && IsXMM(Destination))
            Destination[0..31] = Source[0..31];
            //Destination[32..127] remains unchanged
            //MOVSS instruction when source operand is XMM register and destination operand is memory location:
        else if(IsXMM(Source) && IsMemory(Destination))
            Destination = Source[0..31];
        //MOVSS instruction when source operand is memory location and destination operand is XMM register:
        else {
                Destination[0..31] = Source;
                Destination[32..127] = 0;
        }
        """
        if dest.type == 'register' and src.type == 'register':
            assert dest.size == 128 and src.size == 128
            dest.write(dest.read() & ~0xffffffff | src.read() & 0xffffffff)
        elif dest.type == 'memory':
            assert src.type == 'register'
            dest.write(Operators.EXTRACT(src.read(), 0, dest.size))
        else:
            assert src.type == 'memory' and dest.type == 'register'
            assert src.size == 32 and dest.size == 128
            dest.write(Operators.ZEXTEND(src.read(), 128))