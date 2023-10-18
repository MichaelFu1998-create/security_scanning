def sigma(self):
        r'''Surface tension of the mixture at its current temperature and
        composition, in units of [N/m].

        For calculation of this property at other temperatures,
        or specifying manually the method used to calculate it, and more - see
        the object oriented interface :obj:`thermo.interface.SurfaceTensionMixture`;
        each Mixture instance creates one to actually perform the calculations.

        Examples
        --------
        >>> Mixture(['water'], ws=[1], T=300, P=1E5).sigma
        0.07176932405246211
        '''
        return self.SurfaceTensionMixture(self.T, self.P, self.zs, self.ws)