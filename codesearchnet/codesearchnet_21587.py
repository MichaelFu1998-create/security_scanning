def combine(self, members, output_file, dimension=None, start_index=None, stop_index=None, stride=None):
        """ Combine many files into a single file on disk.  Defaults to using the 'time' dimension. """
        nco = None
        try:
            nco = Nco()
        except BaseException:
            # This is not necessarily an import error (could be wrong PATH)
            raise ImportError("NCO not found.  The NCO python bindings are required to use 'Collection.combine'.")

        if len(members) > 0 and hasattr(members[0], 'path'):
            # A member DotDoct was passed in, we only need the paths
            members = [ m.path for m in members ]

        options  = ['-4']  # NetCDF4
        options += ['-L', '3']  # Level 3 compression
        options += ['-h']  # Don't append to the history global attribute
        if dimension is not None:
            if start_index is None:
                start_index = 0
            if stop_index is None:
                stop_index = ''
            if stride is None:
                stride = 1
            options += ['-d', '{0},{1},{2},{3}'.format(dimension, start_index, stop_index, stride)]
        nco.ncrcat(input=members, output=output_file, options=options)