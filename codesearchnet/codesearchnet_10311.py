def cat(self, out_ndx=None):
        """Concatenate input index files.

        Generate a new index file that contains the default Gromacs index
        groups (if a structure file was defined) and all index groups from the
        input index files.

        :Arguments:
           out_ndx : filename
              Name of the output index file; if ``None`` then use the default
              provided to the constructore. [``None``].
        """
        if out_ndx is None:
            out_ndx = self.output
        self.make_ndx(o=out_ndx, input=['q'])
        return out_ndx