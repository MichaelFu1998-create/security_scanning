def csi(self, capname, *args):
        """Return the escape sequence for the selected Control Sequence."""
        value = curses.tigetstr(capname)
        if value is None:
            return b''
        else:
            return curses.tparm(value, *args)