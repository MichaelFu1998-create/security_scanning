def Vfgs(self, T=None, P=None):
        r'''Volume fractions of all species in a hypothetical pure-gas phase 
        at the current or specified temperature and pressure. If temperature 
        or pressure are specified, the non-specified property is assumed to be 
        that of the mixture. Note this is a method, not a property. Volume 
        fractions are calculated based on **pure species volumes only**.

        Examples
        --------
        >>> Mixture(['sulfur hexafluoride', 'methane'], zs=[.2, .9], T=315).Vfgs()
        [0.18062059238682632, 0.8193794076131737]
        
        >>> S = Mixture(['sulfur hexafluoride', 'methane'], zs=[.1, .9])
        >>> S.Vfgs(P=1E2)
        [0.0999987466608421, 0.9000012533391578]
        '''
        if (T is None or T == self.T) and (P is None or P == self.P):
            Vmgs = self.Vmgs
        else:
            if T is None: T = self.T
            if P is None: P = self.P
            Vmgs = [i(T, P) for i in self.VolumeGases]
        if none_and_length_check([Vmgs]):
            return zs_to_Vfs(self.zs, Vmgs)
        return None