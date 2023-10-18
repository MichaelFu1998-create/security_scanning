def _LDM(cpu, insn_id, base, regs):
        """
        LDM (Load Multiple) loads a non-empty subset, or possibly all, of the general-purpose registers from
        sequential memory locations. It is useful for block loads, stack operations and procedure exit sequences.

        :param int insn_id: should be one of ARM_INS_LDM, ARM_INS_LDMIB, ARM_INS_LDMDA, ARM_INS_LDMDB
        :param Armv7Operand base: Specifies the base register.
        :param list[Armv7Operand] regs:
            Is a list of registers. It specifies the set of registers to be loaded by the LDM instruction.
            The registers are loaded in sequence, the lowest-numbered register from the lowest memory
            address (start_address), through to the highest-numbered register from the highest memory
            address (end_address). If the PC is specified in the register list (opcode bit[15] is set),
            the instruction causes a branch to the address (data) loaded into the PC.

        It's technically UNKNOWN if you writeback to a register you loaded into, but we let it slide.
        """
        if cpu.instruction.usermode:
            raise NotImplementedError("Use of the S bit is not supported")

        increment = insn_id in (cs.arm.ARM_INS_LDM, cs.arm.ARM_INS_LDMIB)
        after = insn_id in (cs.arm.ARM_INS_LDM, cs.arm.ARM_INS_LDMDA)

        address = base.read()

        for reg in regs:
            if not after:
                address += (1 if increment else -1) * (reg.size // 8)

            reg.write(cpu.read_int(address, reg.size))
            if reg.reg in ('PC', 'R15'):
                # The general-purpose registers loaded can include the PC. If they do, the word loaded for the PC is
                # treated as an address and a branch occurs to that address. In ARMv5 and above, bit[0] of the loaded
                # value determines whether execution continues after this branch in ARM state or in Thumb state, as
                # though a BX instruction had been executed.
                cpu._set_mode_by_val(cpu.PC)
                cpu.PC = cpu.PC & ~1

            if after:
                address += (1 if increment else -1) * (reg.size // 8)

        if cpu.instruction.writeback:
            base.writeback(address)