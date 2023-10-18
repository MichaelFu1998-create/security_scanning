def _mpsse_enable(self):
        """Enable MPSSE mode on the FTDI device."""
        # Reset MPSSE by sending mask = 0 and mode = 0
        self._check(ftdi.set_bitmode, 0, 0)
        # Enable MPSSE by sending mask = 0 and mode = 2
        self._check(ftdi.set_bitmode, 0, 2)