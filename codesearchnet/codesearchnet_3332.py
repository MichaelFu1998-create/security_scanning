def PSRLQ(cpu, dest, src):
        """Shift Packed Data Right Logical

        Shifts the bits in the individual quadword in the destination operand to the right by
        the number of bits specified in the count operand . As the bits in the data elements
        are shifted right, the empty high-order bits are cleared (set to 0). If the value
        specified by the count operand is greater than  63, then the destination operand is set
        to all 0s.

        if(OperandSize == 64) {
                        //PSRLQ instruction with 64-bit operand:
                        if(Count > 63) Destination[64..0] = 0;
                        else Destination = ZeroExtend(Destination >> Count);
                }
                else {
                        //PSRLQ instruction with 128-bit operand:
                        if(Count > 15) Destination[128..0] = 0;
                        else {
                                Destination[0..63] = ZeroExtend(Destination[0..63] >> Count);
                                Destination[64..127] = ZeroExtend(Destination[64..127] >> Count);
                        }
                }
        """

        count = src.read()
        count = Operators.ITEBV(src.size, Operators.UGT(count, 63), 64, count)
        count = Operators.EXTRACT(count, 0, 64)
        if dest.size == 64:
            dest.write(dest.read() >> count)
        else:
            hi = Operators.EXTRACT(dest.read(), 64, 64) >> count
            low = Operators.EXTRACT(dest.read(), 0, 64) >> count
            dest.write(Operators.CONCAT(128, hi, low))