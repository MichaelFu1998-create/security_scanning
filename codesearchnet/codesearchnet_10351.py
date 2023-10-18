def parse(self):
        """Parse the xpm file and populate :attr:`XPM.array`."""
        with utilities.openany(self.real_filename) as xpm:
            # Read in lines until we find the start of the array
            meta = [xpm.readline()]
            while not meta[-1].startswith("static char *gromacs_xpm[]"):
                meta.append(xpm.readline())

            # The next line will contain the dimensions of the array
            dim = xpm.readline()
            # There are four integers surrounded by quotes
            # nx: points along x, ny: points along y, nc: ?, nb: stride x
            nx, ny, nc, nb = [int(i) for i in self.unquote(dim).split()]

            # The next dim[2] lines contain the color definitions
            # Each pixel is encoded by dim[3] bytes, and a comment
            # at the end of the line contains the corresponding value
            colors = dict([self.col(xpm.readline()) for i in range(nc)])


            if self.autoconvert:
                autoconverter = Autoconverter(mode="singlet")
                for symbol, value in colors.items():
                    colors[symbol] = autoconverter.convert(value)
                self.logger.debug("Autoconverted colours: %r", colors)

            # make an array containing all possible values and let numpy figure out the dtype
            dtype = numpy.array(colors.values()).dtype
            self.logger.debug("Guessed array type: %s", dtype.name)

            # pre-allocate array
            data = numpy.zeros((int(nx/nb), ny), dtype=dtype)

            self.logger.debug("dimensions: NX=%d NY=%d strideX=%d (NC=%d) --> (%d, %d)",
                              nx, ny, nb, nc, nx/nb, ny)

            iy = 0
            xval = []
            yval = []
            autoconverter = Autoconverter(mode="singlet")
            for line in xpm:
                if line.startswith("/*"):
                    # lines '/* x-axis:' ... and '/* y-axis:' contain the
                    # values of x and y coordinates
                    s = self.uncomment(line).strip()
                    if s.startswith('x-axis:'):
                        xval.extend([autoconverter.convert(x) for x in s[7:].split()])
                    elif s.startswith('y-axis:'):
                        yval.extend([autoconverter.convert(y) for y in s[7:].split()])
                    continue
                s = self.unquote(line)
                # Joao M. Damas <jmdamas@itqb.unl.pt> suggests on gmx-users (24 Oct 2014)
                # that the next line should read:
                #
                #  data[:, iy]  =  [colors[j[k:k+nb]] for k in range(0,nx*nb,nb)]
                #
                # "if one is using higher -nlevels for the .xpm construction (in g_rms, for example)"
                # However, without a test case I am not eager to change it right away so in
                # case some faulty behavior is discovered with the XPM reader then this comment
                # might be helpful. --- Oliver 2014-10-25
                data[:, iy] = [colors[s[k:k+nb]] for k in range(0,nx,nb)]
                self.logger.debug("read row %d with %d columns: '%s....%s'",
                                  iy, data.shape[0], s[:4], s[-4:])
                iy += 1  # for next row

        self.xvalues = numpy.array(xval)
        if self.reverse:
            self.logger.debug("reversed row order, reverse=%r", self.reverse)
            self.__array = data[:, ::-1]
            self.yvalues = numpy.array(yval)
        else:
            self.__array = data
            self.yvalues = numpy.array(yval)[::-1]