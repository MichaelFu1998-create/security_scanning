def draw_2d(self, width=300, height=300, Hs=False): # pragma: no cover
        r'''Interface for drawing a 2D image of the molecule.
        Requires an HTML5 browser, and the libraries RDKit and
        IPython. An exception is raised if either of these libraries is
        absent.

        Parameters
        ----------
        width : int
            Number of pixels wide for the view
        height : int
            Number of pixels tall for the view
        Hs : bool
            Whether or not to show hydrogen

        Examples
        --------
        >>> Chemical('decane').draw_2d() # doctest: +ELLIPSIS
        <PIL.Image.Image image mode=RGBA size=300x300 at 0x...>
        '''
        try:
            from rdkit.Chem import Draw
            from rdkit.Chem.Draw import IPythonConsole
            if Hs:
                mol = self.rdkitmol_Hs
            else:
                mol = self.rdkitmol
            return Draw.MolToImage(mol, size=(width, height))
        except:
            return 'Rdkit is required for this feature.'