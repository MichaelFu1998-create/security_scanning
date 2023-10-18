def copy_memory(self, address, size):
        """
        Copy the bytes from address to address+size into Unicorn
        Used primarily for copying memory maps
        :param address: start of buffer to copy
        :param size: How many bytes to copy
        """
        start_time = time.time()
        map_bytes = self._cpu._raw_read(address, size)
        self._emu.mem_write(address, map_bytes)
        if time.time() - start_time > 3:
            logger.info(f"Copying {hr_size(size)} map at {hex(address)} took {time.time() - start_time} seconds")