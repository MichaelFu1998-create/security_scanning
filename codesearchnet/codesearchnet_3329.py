def VEXTRACTF128(cpu, dest, src, offset):
        """Extract Packed Floating-Point Values

        Extracts 128-bits of packed floating-point values from the source
        operand (second operand) at an 128-bit offset from imm8[0] into the
        destination operand (first operand). The destination may be either an
        XMM register or an 128-bit memory location.
        """
        offset = offset.read()
        dest.write(Operators.EXTRACT(src.read(), offset * 128, (offset + 1) * 128))