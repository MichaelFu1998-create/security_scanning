def _hook_xfer_mem(self, uc, access, address, size, value, data):
        """
        Handle memory operations from unicorn.
        """
        assert access in (UC_MEM_WRITE, UC_MEM_READ, UC_MEM_FETCH)

        if access == UC_MEM_WRITE:
            self._cpu.write_int(address, value, size * 8)

        # If client code is attempting to read a value, we need to bring it
        # in from Manticore state. If we try to mem_write it here, Unicorn
        # will segfault. We add the value to a list of things that need to
        # be written, and ask to restart the emulation.
        elif access == UC_MEM_READ:
            value = self._cpu.read_bytes(address, size)

            if address in self._should_be_written:
                return True

            self._should_be_written[address] = value

            self._should_try_again = True
            return False

        return True