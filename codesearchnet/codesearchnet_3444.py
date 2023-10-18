def _hook_unmapped(self, uc, access, address, size, value, data):
        """
        We hit an unmapped region; map it into unicorn.
        """
        try:
            self.sync_unicorn_to_manticore()
            logger.warning(f"Encountered an operation on unmapped memory at {hex(address)}")
            m = self._cpu.memory.map_containing(address)
            self.copy_memory(m.start, m.end - m.start)
        except MemoryException as e:
            logger.error("Failed to map memory {}-{}, ({}): {}".format(hex(address), hex(address + size), access, e))
            self._to_raise = e
            self._should_try_again = False
            return False

        self._should_try_again = True
        return False