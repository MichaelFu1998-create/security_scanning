def get_arrays(self, lines, personalities=[]):
        """Return a dict of arrays."""
        ret = {}

        i = 0
        while i < len(lines):
            try:
                # First array line: get the md device
                md_device = self.get_md_device_name(lines[i])
            except IndexError:
                # No array detected
                pass
            else:
                # Array detected
                if md_device is not None:
                    # md device line
                    ret[md_device] = self.get_md_device(lines[i], personalities)
                    # md config/status line
                    i += 1
                    ret[md_device].update(self.get_md_status(lines[i]))
            i += 1

        return ret