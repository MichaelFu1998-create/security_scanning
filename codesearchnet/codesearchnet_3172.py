def execute(self):
        """
        Decode, and execute one instruction pointed by register PC
        """
        if issymbolic(self.PC):
            raise ConcretizeRegister(self, 'PC', policy='ALL')

        if not self.memory.access_ok(self.PC, 'x'):
            raise InvalidMemoryAccess(self.PC, 'x')

        self._publish('will_decode_instruction', self.PC)

        insn = self.decode_instruction(self.PC)
        self._last_pc = self.PC

        self._publish('will_execute_instruction', self.PC, insn)

        # FIXME (theo) why just return here?
        if insn.address != self.PC:
            return

        name = self.canonicalize_instruction_name(insn)

        if logger.level == logging.DEBUG:
            logger.debug(self.render_instruction(insn))
            for l in self.render_registers():
                register_logger.debug(l)

        try:
            if self._concrete and 'SYSCALL' in name:
                self.emu.sync_unicorn_to_manticore()
            if self._concrete and 'SYSCALL' not in name:
                self.emulate(insn)
                if self.PC == self._break_unicorn_at:
                    logger.debug("Switching from Unicorn to Manticore")
                    self._break_unicorn_at = None
                    self._concrete = False
            else:
                implementation = getattr(self, name, None)

                if implementation is not None:
                    implementation(*insn.operands)

                else:
                    text_bytes = ' '.join('%02x' % x for x in insn.bytes)
                    logger.warning("Unimplemented instruction: 0x%016x:\t%s\t%s\t%s",
                                   insn.address, text_bytes, insn.mnemonic, insn.op_str)
                    self.backup_emulate(insn)
        except (Interruption, Syscall) as e:
            e.on_handled = lambda: self._publish_instruction_as_executed(insn)
            raise e
        else:
            self._publish_instruction_as_executed(insn)