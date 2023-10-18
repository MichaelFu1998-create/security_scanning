def rdkitmol_Hs(self):
        r'''RDKit object of the chemical, with hydrogen. If RDKit is not
        available, holds None.

        For examples of what can be done with RDKit, see
        `their website <http://www.rdkit.org/docs/GettingStartedInPython.html>`_.
        '''
        if self.__rdkitmol_Hs:
            return self.__rdkitmol_Hs
        else:
            try:
                self.__rdkitmol_Hs = Chem.AddHs(self.rdkitmol)
                return self.__rdkitmol_Hs
            except:
                return None