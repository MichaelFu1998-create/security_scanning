def renumber_atoms(self):
        """Reset the molecule's atoms :attr:`number` to be 1-indexed"""
        if self.atoms:

            # reset the mapping
            self._anumb_to_atom = {}

            for i,atom in enumerate(self.atoms):
                atom.number = i+1   # starting from 1

        else:
            self.logger("the number of atoms is zero - no renumbering")