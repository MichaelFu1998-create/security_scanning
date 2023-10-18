def get_terminal_size(default_cols=80, default_rows=25):
    """Return current terminal size (cols, rows) or a default if detect fails.

    This snippet comes from color ls by Chuck Blake:
    http://pdos.csail.mit.edu/~cblake/cls/cls.py

    """
    def ioctl_GWINSZ(fd):
        """Get (cols, rows) from a putative fd to a tty."""
        try:                               
            rows_cols = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234')) 
            return tuple(reversed(rows_cols))
        except:
            return None
    # Try std in/out/err...
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    # ...or ctty...
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            # ...or fall back to defaults
            cr = (int(os.environ.get('COLUMNS', default_cols)), 
                  int(os.environ.get('LINES', default_rows)))
    return cr