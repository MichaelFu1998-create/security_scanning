def outfile(self, p):
        """Path for an output file.

        If :attr:`outdir` is set then the path is
        ``outdir/basename(p)`` else just ``p``
        """
        if self.outdir is not None:
            return os.path.join(self.outdir, os.path.basename(p))
        else:
            return p