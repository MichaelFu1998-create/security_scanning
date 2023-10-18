def sys_open(self, buf, flags, mode):
        """
        A version of open(2) that includes a special case for a symbolic path.
        When given a symbolic path, it will create a temporary file with
        64 bytes of symbolic bytes as contents and return that instead.

        :param buf: address of zero-terminated pathname
        :param flags: file access bits
        :param mode: file permission mode
        """
        offset = 0
        symbolic_path = issymbolic(self.current.read_int(buf, 8))
        if symbolic_path:
            import tempfile
            fd, path = tempfile.mkstemp()
            with open(path, 'wb+') as f:
                f.write('+' * 64)
            self.symbolic_files.append(path)
            buf = self.current.memory.mmap(None, 1024, 'rw ', data_init=path)

        rv = super().sys_open(buf, flags, mode)

        if symbolic_path:
            self.current.memory.munmap(buf, 1024)

        return rv