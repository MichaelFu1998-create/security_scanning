def write(self, out_ndx=None, defaultgroups=False):
        """Write individual (named) groups to *out_ndx*."""
        name_all, out_ndx = self.combine(operation=False, out_ndx=out_ndx, defaultgroups=defaultgroups)
        return out_ndx