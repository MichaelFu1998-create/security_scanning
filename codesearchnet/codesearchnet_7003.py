def draw_2d(self,  Hs=False): # pragma: no cover
        r'''Interface for drawing a 2D image of all the molecules in the
        mixture. Requires an HTML5 browser, and the libraries RDKit and
        IPython. An exception is raised if either of these libraries is
        absent.

        Parameters
        ----------
        Hs : bool
            Whether or not to show hydrogen

        Examples
        --------
        Mixture(['natural gas']).draw_2d()
        '''
        try:
            from rdkit.Chem import Draw
            from rdkit.Chem.Draw import IPythonConsole
            if Hs:
                mols = [i.rdkitmol_Hs for i in self.Chemicals]
            else:
                mols = [i.rdkitmol for i in self.Chemicals]
            return Draw.MolsToImage(mols)
        except:
            return 'Rdkit is required for this feature.'