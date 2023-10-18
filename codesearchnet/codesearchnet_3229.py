def LAHF(cpu):
        """
        Loads status flags into AH register.

        Moves the low byte of the EFLAGS register (which includes status flags
        SF, ZF, AF, PF, and CF) to the AH register. Reserved bits 1, 3, and 5
        of the EFLAGS register are set in the AH register::

                AH  =  EFLAGS(SF:ZF:0:AF:0:PF:1:CF);

        :param cpu: current CPU.
        :param dest: destination operand.
        :param src: source operand.
        """
        used_regs = (cpu.SF, cpu.ZF, cpu.AF, cpu.PF, cpu.CF)
        is_expression = any(issymbolic(x) for x in used_regs)

        def make_flag(val, offset):
            if is_expression:
                return Operators.ITEBV(8, val,
                                       BitVecConstant(8, 1 << offset),
                                       BitVecConstant(8, 0))
            else:
                return val << offset

        cpu.AH = (make_flag(cpu.SF, 7) |
                  make_flag(cpu.ZF, 6) |
                  make_flag(0, 5) |
                  make_flag(cpu.AF, 4) |
                  make_flag(0, 3) |
                  make_flag(cpu.PF, 2) |
                  make_flag(1, 1) |
                  make_flag(cpu.CF, 0))