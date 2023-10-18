def MOV(cpu, dest, src):
        """
        Implement the MOV{S} instruction.

        Note: If src operand is PC, temporarily release our logical PC
        view and conform to the spec, which dictates PC = curr instr + 8

        :param Armv7Operand dest: The destination operand; register.
        :param Armv7Operand src: The source operand; register or immediate.
        """
        if cpu.mode == cs.CS_MODE_ARM:
            result, carry_out = src.read(with_carry=True)
            dest.write(result)
            cpu.set_flags(C=carry_out, N=HighBit(result), Z=(result == 0))
        else:
            # thumb mode cannot do wonky things to the operand, so no carry calculation
            result = src.read()
            dest.write(result)
            cpu.set_flags(N=HighBit(result), Z=(result == 0))