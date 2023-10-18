def write(self, filename=None):
        """Write array to xvg file *filename* in NXY format.

        .. Note:: Only plain files working at the moment, not compressed.
        """
        self._init_filename(filename)
        with utilities.openany(self.real_filename, 'w') as xvg:
            xvg.write("# xmgrace compatible NXY data file\n"
                      "# Written by gromacs.formats.XVG()\n")
            xvg.write("# :columns: {0!r}\n".format(self.names))
            for xyy in self.array.T:
                xyy.tofile(xvg, sep=" ", format="%-8s")  # quick and dirty ascii output...--no compression!
                xvg.write('\n')