def _create_emulated_mapping(self, uc, address):
        """
        Create a mapping in Unicorn and note that we'll need it if we retry.
        :param uc: The Unicorn instance.
        :param address: The address which is contained by the mapping.
        :rtype Map
        """

        m = self._cpu.memory.map_containing(address)

        permissions = UC_PROT_NONE
        if 'r' in m.perms:
            permissions |= UC_PROT_READ
        if 'w' in m.perms:
            permissions |= UC_PROT_WRITE
        if 'x' in m.perms:
            permissions |= UC_PROT_EXEC

        uc.mem_map(m.start, len(m), permissions)

        self._should_be_mapped[m.start] = (len(m), permissions)

        return m