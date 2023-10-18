def sync_unicorn_to_manticore(self):
        """
        Copy registers and written memory back into Manticore
        """
        self.write_backs_disabled = True
        for reg in self.registers:
            val = self._emu.reg_read(self._to_unicorn_id(reg))
            self._cpu.write_register(reg, val)
        if len(self._mem_delta) > 0:
            logger.debug(f"Syncing {len(self._mem_delta)} writes back into Manticore")
        for location in self._mem_delta:
            value, size = self._mem_delta[location]
            self._cpu.write_int(location, value, size * 8)
        self.write_backs_disabled = False
        self._mem_delta = {}