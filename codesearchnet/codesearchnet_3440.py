def unmap_memory_callback(self, start, size):
        """Unmap Unicorn maps when Manticore unmaps them"""
        logger.info(f"Unmapping memory from {hex(start)} to {hex(start + size)}")

        mask = (1 << 12) - 1
        if (start & mask) != 0:
            logger.error("Memory to be unmapped is not aligned to a page")

        if (size & mask) != 0:
            size = ((size >> 12) + 1) << 12
            logger.warning("Forcing unmap size to align to a page")

        self._emu.mem_unmap(start, size)