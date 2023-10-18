def assemble_topology(self):
        """Call the various member self._make_* functions to convert the topology object into a string"""
        self.logger.debug("starting to assemble topology...")

        top = ''

        self.logger.debug("making atom/pair/bond/angle/dihedral/improper types")
        top += self.toptemplate
        top = top.replace('*DEFAULTS*',       ''.join( self._make_defaults(self.system)) )
        top = top.replace('*ATOMTYPES*',      ''.join( self._make_atomtypes(self.system)) )
        top = top.replace('*NONBOND_PARAM*',  ''.join( self._make_nonbond_param(self.system)) )
        top = top.replace('*PAIRTYPES*',      ''.join( self._make_pairtypes(self.system)) )
        top = top.replace('*BONDTYPES*',      ''.join( self._make_bondtypes(self.system)) )
        top = top.replace('*CONSTRAINTTYPES*',''.join( self._make_constrainttypes(self.system)))
        top = top.replace('*ANGLETYPES*',     ''.join( self._make_angletypes(self.system)))
        top = top.replace('*DIHEDRALTYPES*',  ''.join( self._make_dihedraltypes(self.system)) )
        top = top.replace('*IMPROPERTYPES*',  ''.join( self._make_impropertypes(self.system)) )
        top = top.replace('*CMAPTYPES*',      ''.join( self._make_cmaptypes(self.system)) )

        for i,(molname,m) in enumerate(self.system.dict_molname_mol.items()):

            itp = self.itptemplate
            itp = itp.replace('*MOLECULETYPE*',  ''.join( self._make_moleculetype(m, molname, m.exclusion_numb))  )
            itp = itp.replace('*ATOMS*',         ''.join( self._make_atoms(m))  )
            itp = itp.replace('*BONDS*',         ''.join( self._make_bonds(m))  )
            itp = itp.replace('*PAIRS*',         ''.join( self._make_pairs(m))  )
            itp = itp.replace('*SETTLES*',       ''.join( self._make_settles(m))  )
            itp = itp.replace('*VIRTUAL_SITES3*',''.join( self._make_virtual_sites3(m))  )
            itp = itp.replace('*EXCLUSIONS*',    ''.join( self._make_exclusions(m))  )
            itp = itp.replace('*ANGLES*',        ''.join( self._make_angles(m)) )
            itp = itp.replace('*DIHEDRALS*',     ''.join( self._make_dihedrals(m)) )
            itp = itp.replace('*IMPROPERS*',     ''.join( self._make_impropers(m)) )
            itp = itp.replace('*CMAPS*',         ''.join( self._make_cmaps(m)) )
            if not self.multiple_output:
                top += itp
            else:
                outfile = "mol_{0}.itp".format(molname)
                top += '#include "mol_{0}.itp" \n'.format( molname )
                with open(outfile, "w") as f:
                    f.writelines([itp])

        top += '\n[system]  \nConvertedSystem\n\n'
        top += '[molecules] \n'
        molecules = [("", 0)]

        for m in self.system.molecules:
            if (molecules[-1][0] != m.name):
                molecules.append([m.name, 0])
            if molecules[-1][0] == m.name:
                molecules[-1][1] += 1

        for molname, n in molecules[1:]:
            top += '{0:s}     {1:d}\n'.format(molname, n)
        top += '\n'

        with open(self.outfile, 'w') as f:
            f.writelines([top])