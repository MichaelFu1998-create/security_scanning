def _step(self, instruction):
        """
        A single attempt at executing an instruction.
        """
        logger.debug("0x%x:\t%s\t%s"
                     % (instruction.address, instruction.mnemonic, instruction.op_str))

        registers = set(self._cpu.canonical_registers)

        # Refer to EFLAGS instead of individual flags for x86
        if self._cpu.arch == CS_ARCH_X86:
            # The last 8 canonical registers of x86 are individual flags; replace
            # with the eflags
            registers -= set(['CF', 'PF', 'AF', 'ZF', 'SF', 'IF', 'DF', 'OF'])
            registers.add('EFLAGS')

            # TODO(mark): Unicorn 1.0.1 does not support reading YMM registers,
            # and simply returns back zero. If a unicorn emulated instruction writes to an
            # XMM reg, we will read back the corresponding YMM register, resulting in an
            # incorrect zero value being actually written to the XMM register. This is
            # fixed in Unicorn PR #819, so when that is included in a release, delete
            # these two lines.
            registers -= set(['YMM0', 'YMM1', 'YMM2', 'YMM3', 'YMM4', 'YMM5', 'YMM6', 'YMM7',
                              'YMM8', 'YMM9', 'YMM10', 'YMM11', 'YMM12', 'YMM13', 'YMM14', 'YMM15'])
            registers |= set(['XMM0', 'XMM1', 'XMM2', 'XMM3', 'XMM4', 'XMM5', 'XMM6', 'XMM7',
                              'XMM8', 'XMM9', 'XMM10', 'XMM11', 'XMM12', 'XMM13', 'XMM14', 'XMM15'])

        # XXX(yan): This concretizes the entire register state. This is overly
        # aggressive. Once capstone adds consistent support for accessing
        # referred registers, make this only concretize those registers being
        # read from.
        for reg in registers:
            val = self._cpu.read_register(reg)
            if issymbolic(val):
                from ..native.cpu.abstractcpu import ConcretizeRegister
                raise ConcretizeRegister(self._cpu, reg, "Concretizing for emulation.",
                                         policy='ONE')
            self._emu.reg_write(self._to_unicorn_id(reg), val)

        # Bring in the instruction itself
        instruction = self._cpu.decode_instruction(self._cpu.PC)
        text_bytes = self._cpu.read_bytes(self._cpu.PC, instruction.size)
        self._emu.mem_write(self._cpu.PC, b''.join(text_bytes))

        self._emu.hook_add(UC_HOOK_MEM_READ_UNMAPPED, self._hook_unmapped)
        self._emu.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, self._hook_unmapped)
        self._emu.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, self._hook_unmapped)
        self._emu.hook_add(UC_HOOK_MEM_READ, self._hook_xfer_mem)
        self._emu.hook_add(UC_HOOK_MEM_WRITE, self._hook_xfer_mem)
        self._emu.hook_add(UC_HOOK_INTR, self._interrupt)

        saved_PC = self._cpu.PC

        try:
            pc = self._cpu.PC
            if self._cpu.arch == CS_ARCH_ARM and self._uc_mode == UC_MODE_THUMB:
                pc |= 1
            self._emu.emu_start(pc, self._cpu.PC + instruction.size, count=1)
        except UcError as e:
            # We request re-execution by signaling error; if we we didn't set
            # _should_try_again, it was likely an actual error
            if not self._should_try_again:
                raise

        if self._should_try_again:
            return

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("=" * 10)
            for register in self._cpu.canonical_registers:
                logger.debug(
                    f"Register {register:3s}  "
                    f"Manticore: {self._cpu.read_register(register):08x}, "
                    f"Unicorn {self._emu.reg_read(self._to_unicorn_id(register)):08x}"
                )
            logger.debug(">" * 10)

        # Bring back Unicorn registers to Manticore
        for reg in registers:
            val = self._emu.reg_read(self._to_unicorn_id(reg))
            self._cpu.write_register(reg, val)

        # Unicorn hack. On single step, unicorn wont advance the PC register
        mu_pc = self.get_unicorn_pc()
        if saved_PC == mu_pc:
            self._cpu.PC = saved_PC + instruction.size

        # Raise the exception from a hook that Unicorn would have eaten
        if self._to_raise:
            raise self._to_raise

        return