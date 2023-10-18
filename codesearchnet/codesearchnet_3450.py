def update_segment(self, selector, base, size, perms):
        """ Only useful for setting FS right now. """
        logger.info("Updating selector %s to 0x%02x (%s bytes) (%s)", selector, base, size, perms)
        if selector == 99:
            self.set_fs(base)
        else:
            logger.error("No way to write segment: %d", selector)