def _translate_residue(self, selection, default_atomname='CA'):
        """Translate selection for a single res to make_ndx syntax."""
        m = self.RESIDUE.match(selection)
        if not m:
            errmsg = "Selection {selection!r} is not valid.".format(**vars())
            logger.error(errmsg)
            raise ValueError(errmsg)

        gmx_resid = self.gmx_resid(int(m.group('resid')))    # magic offset correction
        residue = m.group('aa')
        if len(residue) == 1:
            gmx_resname = utilities.convert_aa_code(residue) # only works for AA
        else:
            gmx_resname = residue                            # use 3-letter for any resname

        gmx_atomname = m.group('atom')
        if gmx_atomname is None:
            gmx_atomname = default_atomname

        return {'resname':gmx_resname, 'resid':gmx_resid, 'atomname':gmx_atomname}