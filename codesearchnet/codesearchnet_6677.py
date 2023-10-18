def draw_3d(self, width=300, height=500, style='stick', Hs=True): # pragma: no cover
        r'''Interface for drawing an interactive 3D view of the molecule.
        Requires an HTML5 browser, and the libraries RDKit, pymol3D, and
        IPython. An exception is raised if all three of these libraries are
        not installed.

        Parameters
        ----------
        width : int
            Number of pixels wide for the view
        height : int
            Number of pixels tall for the view
        style : str
            One of 'stick', 'line', 'cross', or 'sphere'
        Hs : bool
            Whether or not to show hydrogen

        Examples
        --------
        >>> Chemical('cubane').draw_3d()
        <IPython.core.display.HTML object>
        '''
        try:
            import py3Dmol
            from IPython.display import display
            if Hs:
                mol = self.rdkitmol_Hs
            else:
                mol = self.rdkitmol
            AllChem.EmbedMultipleConfs(mol)
            mb = Chem.MolToMolBlock(mol)
            p = py3Dmol.view(width=width,height=height)
            p.addModel(mb,'sdf')
            p.setStyle({style:{}})
            p.zoomTo()
            display(p.show())
        except:
            return 'py3Dmol, RDKit, and IPython are required for this feature.'