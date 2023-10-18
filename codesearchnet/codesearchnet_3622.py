def _get_expand_imm_carry(self, carryIn):
        """Manually compute the carry bit produced by expanding an immediate operand (see ARMExpandImm_C)"""
        insn = struct.unpack('<I', self.cpu.instruction.bytes)[0]
        unrotated = insn & Mask(8)
        shift = Operators.EXTRACT(insn, 8, 4)
        _, carry = self.cpu._shift(unrotated, cs.arm.ARM_SFT_ROR, 2 * shift, carryIn)
        return carry