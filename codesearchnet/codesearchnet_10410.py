def parse(self, stride=None):
        """Read and cache the file as a numpy array.

        Store every *stride* line of data; if ``None`` then the class default is used.

        The array is returned with column-first indexing, i.e. for a data file with
        columns X Y1 Y2 Y3 ... the array a will be a[0] = X, a[1] = Y1, ... .
        """
        if stride is None:
            stride = self.stride
        self.corrupted_lineno = []
        irow  = 0  # count rows of data
        # cannot use numpy.loadtxt() because xvg can have two types of 'comment' lines
        with utilities.openany(self.real_filename) as xvg:
            rows = []
            ncol = None
            for lineno,line in enumerate(xvg):
                line = line.strip()
                if len(line) == 0:
                    continue
                if "label" in line and "xaxis" in line:
                        self.xaxis = line.split('"')[-2]
                if "label" in line and "yaxis" in line:
                        self.yaxis = line.split('"')[-2]
                if line.startswith("@ legend"):
                                        if not "legend" in self.metadata: self.metadata["legend"] = []
                                        self.metadata["legend"].append(line.split("legend ")[-1])
                if line.startswith("@ s") and "subtitle" not in line:
                                        name = line.split("legend ")[-1].replace('"','').strip()
                                        self.names.append(name)
                if line.startswith(('#', '@')) :
                                        continue
                if line.startswith('&'):
                    raise NotImplementedError('{0!s}: Multi-data not supported, only simple NXY format.'.format(self.real_filename))
                # parse line as floats
                try:
                    row = [float(el) for el in line.split()]
                except:
                    if self.permissive:
                        self.logger.warn("%s: SKIPPING unparsable line %d: %r",
                                         self.real_filename, lineno+1, line)
                        self.corrupted_lineno.append(lineno+1)
                        continue
                    self.logger.error("%s: Cannot parse line %d: %r",
                                      self.real_filename, lineno+1, line)
                    raise
                # check for same number of columns as in previous step
                if ncol is not None and len(row) != ncol:
                    if self.permissive:
                        self.logger.warn("%s: SKIPPING line %d with wrong number of columns: %r",
                                         self.real_filename, lineno+1, line)
                        self.corrupted_lineno.append(lineno+1)
                        continue
                    errmsg = "{0!s}: Wrong number of columns in line {1:d}: {2!r}".format(self.real_filename, lineno+1, line)
                    self.logger.error(errmsg)
                    raise IOError(errno.ENODATA, errmsg, self.real_filename)
                # finally: a good line
                if irow % stride == 0:
                    ncol = len(row)
                    rows.append(row)
                irow += 1
        try:
            self.__array = numpy.array(rows).transpose()    # cache result
        except:
            self.logger.error("%s: Failed reading XVG file, possibly data corrupted. "
                              "Check the last line of the file...", self.real_filename)
            raise
        finally:
            del rows