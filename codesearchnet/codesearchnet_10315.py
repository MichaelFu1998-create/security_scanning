def _process_range(self, selection, name=None):
        """Process a range selection.

        ("S234", "A300", "CA")   --> selected all CA in this range
        ("S234", "A300")         --> selected all atoms in this range

        .. Note:: Ignores residue type, only cares about the resid (but still required)
        """

        try:
            first, last, gmx_atomname = selection
        except ValueError:
            try:
                first, last = selection
                gmx_atomname = '*'
            except:
                logger.error("%r is not a valid range selection", selection)
                raise
        if name is None:
            name = "{first!s}-{last!s}_{gmx_atomname!s}".format(**vars())

        _first = self._translate_residue(first, default_atomname=gmx_atomname)
        _last = self._translate_residue(last, default_atomname=gmx_atomname)

        _selection = 'r {0:d} - {1:d} & & a {2!s}'.format(_first['resid'], _last['resid'], gmx_atomname)
        cmd = ['keep 0', 'del 0',
               _selection,
               'name 0 {name!s}'.format(**vars()),
               'q']
        fd, ndx = tempfile.mkstemp(suffix='.ndx', prefix=name+'__')
        rc,out,err = self.make_ndx(n=self.ndx, o=ndx, input=cmd)
        self.check_output(out, "No atoms found for "
                          "%(selection)r --> %(_selection)r" % vars())
        # For debugging, look at out and err or set stdout=True, stderr=True
        ##print "DEBUG: _process_residue()"
        ##print out

        return name, ndx