def _STM(cpu, insn_id, base, regs):
        """
        STM (Store Multiple) stores a non-empty subset (or possibly all) of the general-purpose registers to
        sequential memory locations.

        :param int insn_id: should be one of ARM_INS_STM, ARM_INS_STMIB, ARM_INS_STMDA, ARM_INS_STMDB
        :param Armv7Operand base: Specifies the base register.
        :param list[Armv7Operand] regs:
            Is a list of registers. It specifies the set of registers to be stored by the STM instruction.
            The registers are stored in sequence, the lowest-numbered register to the lowest
            memory address (start_address), through to the highest-numbered register to the
            highest memory address (end_address).
        """
        if cpu.instruction.usermode:
            raise NotImplementedError("Use of the S bit is not supported")

        increment = insn_id in (cs.arm.ARM_INS_STM, cs.arm.ARM_INS_STMIB)
        after = insn_id in (cs.arm.ARM_INS_STM, cs.arm.ARM_INS_STMDA)

        address = base.read()

        for reg in regs:
            if not after:
                address += (1 if increment else -1) * (reg.size // 8)

            cpu.write_int(address, reg.read(), reg.size)

            if after:
                address += (1 if increment else -1) * (reg.size // 8)

        if cpu.instruction.writeback:
            base.writeback(address)