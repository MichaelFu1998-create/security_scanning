def write(self, file):
        """Write the *class array* section.

        Parameters
        ----------
        file : file

        Raises
        ------
        ValueError
             If the `dxtype` is not a valid type, :exc:`ValueError` is
             raised.

        """
        if self.type not in self.dx_types:
            raise ValueError(("DX type {} is not supported in the DX format. \n"
                              "Supported valus are: {}\n"
                              "Use the type=<type> keyword argument.").format(
                                  self.type, list(self.dx_types.keys())))
        typelabel = (self.typequote+self.type+self.typequote)
        DXclass.write(self,file,
                      'type {0} rank 0 items {1} data follows'.format(
                          typelabel, self.array.size))
        # grid data, serialized as a C array (z fastest varying)
        # (flat iterator is equivalent to: for x: for y: for z: grid[x,y,z])
        # VMD's DX reader requires exactly 3 values per line
        fmt_string = "{:d}"
        if (self.array.dtype.kind == 'f' or self.array.dtype.kind == 'c'):
            precision = numpy.finfo(self.array.dtype).precision
            fmt_string = "{:."+"{:d}".format(precision)+"f}"
        values_per_line = 3
        values = self.array.flat
        while 1:
            try:
                for i in range(values_per_line):
                    file.write(fmt_string.format(next(values)) + "\t")
                file.write('\n')
            except StopIteration:
                file.write('\n')
                break
        file.write('attribute "dep" string "positions"\n')