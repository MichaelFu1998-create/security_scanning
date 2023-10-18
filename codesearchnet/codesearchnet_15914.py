def _open(self, archive):
        """Open RAR archive file."""
        try:
            handle = unrarlib.RAROpenArchiveEx(ctypes.byref(archive))
        except unrarlib.UnrarException:
            raise BadRarFile("Invalid RAR file.")
        return handle