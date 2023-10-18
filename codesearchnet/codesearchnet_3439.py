def map_memory_callback(self, address, size, perms, name, offset, result):
        """
        Catches did_map_memory and copies the mapping into Manticore
        """
        logger.info(' '.join(("Mapping Memory @",
                              hex(address) if type(address) is int else "0x??",
                              hr_size(size), "-",
                              perms, "-",
                              f"{name}:{hex(offset) if name else ''}", "->",
                              hex(result))))
        self._emu.mem_map(address, size, convert_permissions(perms))
        self.copy_memory(address, size)