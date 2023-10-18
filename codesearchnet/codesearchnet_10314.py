def _process_residue(self, selection, name=None):
        """Process residue/atom selection and return name and temp index file."""

        if name is None:
            name = selection.replace(':', '_')

        # XXX: use _translate_residue() ....
        m = self.RESIDUE.match(selection)
        if not m:
            raise ValueError("Selection {selection!r} is not valid.".format(**vars()))

        gmx_resid = self.gmx_resid(int(m.group('resid')))
        residue = m.group('aa')
        if len(residue) == 1:
            gmx_resname = utilities.convert_aa_code(residue) # only works for AA
        else:
            gmx_resname = residue                            # use 3-letter for any resname
        gmx_atomname = m.group('atom')
        if gmx_atomname is None:
            gmx_atomname = 'CA'

        #: select residue <gmx_resname><gmx_resid> atom <gmx_atomname>
        _selection = 'r {gmx_resid:d} & r {gmx_resname!s} & a {gmx_atomname!s}'.format(**vars())
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