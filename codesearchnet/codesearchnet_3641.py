def _SR(cpu, insn_id, dest, op, *rest):
        """
        Notes on Capstone behavior:
        - In ARM mode, _SR reg has `rest`, but _SR imm does not, its baked into `op`.
        - In ARM mode, `lsr r1, r2` will have a `rest[0]`
        - In Thumb mode, `lsr r1, r2` will have an empty `rest`
        - In ARM mode, something like `lsr r1, 3` will not have `rest` and op will be
            the immediate.
        """
        assert insn_id in (cs.arm.ARM_INS_ASR, cs.arm.ARM_INS_LSL, cs.arm.ARM_INS_LSR)

        if insn_id == cs.arm.ARM_INS_ASR:
            if rest and rest[0].type == 'immediate':
                srtype = cs.arm.ARM_SFT_ASR
            else:
                srtype = cs.arm.ARM_SFT_ASR_REG
        elif insn_id == cs.arm.ARM_INS_LSL:
            if rest and rest[0].type == 'immediate':
                srtype = cs.arm.ARM_SFT_LSL
            else:
                srtype = cs.arm.ARM_SFT_LSL_REG
        elif insn_id == cs.arm.ARM_INS_LSR:
            if rest and rest[0].type == 'immediate':
                srtype = cs.arm.ARM_SFT_LSR
            else:
                srtype = cs.arm.ARM_SFT_LSR_REG

        carry = cpu.regfile.read('APSR_C')
        if rest and rest[0].type == 'register':
            # FIXME we should make Operand.op private (and not accessible)
            result, carry = cpu._shift(op.read(), srtype, rest[0].op.reg, carry)
        elif rest and rest[0].type == 'immediate':
            amount = rest[0].read()
            result, carry = cpu._shift(op.read(), srtype, amount, carry)
        elif cpu.mode == cs.CS_MODE_THUMB:
            result, carry = cpu._shift(dest.read(), srtype, op, carry)
        else:
            result, carry = op.read(with_carry=True)
        dest.write(result)

        cpu.set_flags(N=HighBit(result), Z=(result == 0), C=carry)