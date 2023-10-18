def write_back_register(self, reg, val):
        """ Sync register state from Manticore -> Unicorn"""
        if self.write_backs_disabled:
            return
        if issymbolic(val):
            logger.warning("Skipping Symbolic write-back")
            return
        if reg in self.flag_registers:
            self._emu.reg_write(self._to_unicorn_id('EFLAGS'), self._cpu.read_register('EFLAGS'))
            return
        self._emu.reg_write(self._to_unicorn_id(reg), val)