def sys_mmap_pgoff(self, address, size, prot, flags, fd, offset):
        """Wrapper for mmap2"""
        return self.sys_mmap2(address, size, prot, flags, fd, offset)