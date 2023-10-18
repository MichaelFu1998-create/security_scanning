def _hook_write_mem(self, uc, access, address, size, value, data):
        """
        Captures memory written by Unicorn
        """
        self._mem_delta[address] = (value, size)
        return True