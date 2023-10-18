def protect_memory_callback(self, start, size, perms):
        """ Set memory protections in Unicorn correctly """
        logger.info(f"Changing permissions on {hex(start)}:{hex(start + size)} to {perms}")
        self._emu.mem_protect(start, size, convert_permissions(perms))