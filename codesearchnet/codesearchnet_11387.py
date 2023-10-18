def size(self):
        """Get the current terminal size."""
        for fd in range(3):
            cr = self._ioctl_GWINSZ(fd)
            if cr:
                break
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = self._ioctl_GWINSZ(fd)
                os.close(fd)
            except Exception:
                pass

        if not cr:
            env = os.environ
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        return int(cr[1]), int(cr[0])