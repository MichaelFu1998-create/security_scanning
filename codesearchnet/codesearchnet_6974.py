def Vfls(self, T=None, P=None):
        r'''Volume fractions of all species in a hypothetical pure-liquid phase 
        at the current or specified temperature and pressure. If temperature 
        or pressure are specified, the non-specified property is assumed to be 
        that of the mixture. Note this is a method, not a property. Volume 
        fractions are calculated based on **pure species volumes only**.

        Examples
        --------
        >>> Mixture(['hexane', 'pentane'], zs=[.5, .5], T=315).Vfls()
        [0.5299671144566751, 0.47003288554332484]
        
        >>> S = Mixture(['hexane', 'decane'], zs=[0.25, 0.75])
        >>> S.Vfls(298.16, 101326)
        [0.18301434895886864, 0.8169856510411313]
        '''
        if (T is None or T == self.T) and (P is None or P == self.P):
            Vmls = self.Vmls
        else:
            if T is None: T = self.T
            if P is None: P = self.P
            Vmls = [i(T, P) for i in self.VolumeLiquids]
        if none_and_length_check([Vmls]):
            return zs_to_Vfs(self.zs, Vmls)
        return None