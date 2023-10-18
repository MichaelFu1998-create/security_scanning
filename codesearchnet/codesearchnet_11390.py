def csi_wrap(self, value, capname, *args):
        """Return a value wrapped in the selected CSI and does a reset."""
        if isinstance(value, str):
            value = value.encode('utf-8')
        return b''.join([
            self.csi(capname, *args),
            value,
            self.csi('sgr0'),
        ])