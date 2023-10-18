def _read_header(self, handle):
        """Read current member header into a RarInfo object."""
        header_data = unrarlib.RARHeaderDataEx()
        try:
            res = unrarlib.RARReadHeaderEx(handle, ctypes.byref(header_data))
            rarinfo = RarInfo(header=header_data)
        except unrarlib.ArchiveEnd:
            return None
        except unrarlib.MissingPassword:
            raise RuntimeError("Archive is encrypted, password required")
        except unrarlib.BadPassword:
            raise RuntimeError("Bad password for Archive")
        except unrarlib.UnrarException as e:
            raise BadRarFile(str(e))

        return rarinfo