def to_file(self, outpath):
        """Save this object instance in outpath.

        Parameters
        ----------
        outpath: str
            Output file path
        """
        if not self.has_mask() and not self.is_smoothed():
            save_niigz(outpath, self.img)
        else:
            save_niigz(outpath, self.get_data(masked=True, smoothed=True),
                       self.get_header(), self.get_affine())