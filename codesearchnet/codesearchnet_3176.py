def backup_emulate(self, insn):
        """
        If we could not handle emulating an instruction, use Unicorn to emulate
        it.

        :param capstone.CsInsn instruction: The instruction object to emulate
        """

        if not hasattr(self, 'backup_emu'):
            self.backup_emu = UnicornEmulator(self)
        try:
            self.backup_emu.emulate(insn)
        except unicorn.UcError as e:
            if e.errno == unicorn.UC_ERR_INSN_INVALID:
                text_bytes = ' '.join('%02x' % x for x in insn.bytes)
                logger.error("Unimplemented instruction: 0x%016x:\t%s\t%s\t%s",
                             insn.address, text_bytes, insn.mnemonic, insn.op_str)
            raise InstructionEmulationError(str(e))
        finally:
            # We have been seeing occasional Unicorn issues with it not clearing
            # the backing unicorn instance. Saw fewer issues with the following
            # line present.
            del self.backup_emu