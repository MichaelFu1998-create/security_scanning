def concrete_emulate(self, insn):
        """
        Start executing in Unicorn from this point until we hit a syscall or reach break_unicorn_at

        :param capstone.CsInsn insn: The instruction object to emulate
        """

        if not self.emu:
            self.emu = ConcreteUnicornEmulator(self)
            self.emu._stop_at = self._break_unicorn_at
        try:
            self.emu.emulate(insn)
        except unicorn.UcError as e:
            if e.errno == unicorn.UC_ERR_INSN_INVALID:
                text_bytes = ' '.join('%02x' % x for x in insn.bytes)
                logger.error("Unimplemented instruction: 0x%016x:\t%s\t%s\t%s",
                             insn.address, text_bytes, insn.mnemonic, insn.op_str)
            raise InstructionEmulationError(str(e))