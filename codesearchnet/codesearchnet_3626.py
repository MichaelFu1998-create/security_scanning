def _shift(cpu, value, _type, amount, carry):
        """See Shift() and Shift_C() in the ARM manual"""
        assert(cs.arm.ARM_SFT_INVALID < _type <= cs.arm.ARM_SFT_RRX_REG)

        # XXX: Capstone should set the value of an RRX shift to 1, which is
        # asserted in the manual, but it sets it to 0, so we have to check
        if _type in (cs.arm.ARM_SFT_RRX, cs.arm.ARM_SFT_RRX_REG) and amount != 1:
            amount = 1

        elif _type in range(cs.arm.ARM_SFT_ASR_REG, cs.arm.ARM_SFT_RRX_REG + 1):
            if cpu.mode == cs.CS_MODE_THUMB:
                src = amount.read()
            else:
                src_reg = cpu.instruction.reg_name(amount).upper()
                src = cpu.regfile.read(src_reg)
            amount = Operators.EXTRACT(src, 0, 8)

        if amount == 0:
            return value, carry

        width = cpu.address_bit_size

        if _type in (cs.arm.ARM_SFT_ASR, cs.arm.ARM_SFT_ASR_REG):
            return ASR_C(value, amount, width)
        elif _type in (cs.arm.ARM_SFT_LSL, cs.arm.ARM_SFT_LSL_REG):
            return LSL_C(value, amount, width)
        elif _type in (cs.arm.ARM_SFT_LSR, cs.arm.ARM_SFT_LSR_REG):
            return LSR_C(value, amount, width)
        elif _type in (cs.arm.ARM_SFT_ROR, cs.arm.ARM_SFT_ROR_REG):
            return ROR_C(value, amount, width)
        elif _type in (cs.arm.ARM_SFT_RRX, cs.arm.ARM_SFT_RRX_REG):
            return RRX_C(value, carry, width)

        raise NotImplementedError("Bad shift value")