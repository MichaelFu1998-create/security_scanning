def rdkitmol(self):
        r'''RDKit object of the chemical, without hydrogen. If RDKit is not
        available, holds None.

        For examples of what can be done with RDKit, see
        `their website <http://www.rdkit.org/docs/GettingStartedInPython.html>`_.
        '''
        if self.__rdkitmol:
            return self.__rdkitmol
        else:
            try:
                self.__rdkitmol = Chem.MolFromSmiles(self.smiles)
                return self.__rdkitmol
            except:
                return None