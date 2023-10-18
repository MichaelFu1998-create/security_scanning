def charge_balance(self):
        r'''Charge imbalance of the mixture, in units of [faraday].
        Mixtures meeting the electroneutrality condition will have an imbalance
        of 0.

        Examples
        --------
        >>> Mixture(['Na+', 'Cl-', 'water'], zs=[.01, .01, .98]).charge_balance
        0.0
        '''
        return sum([zi*ci for zi, ci in zip(self.zs, self.charges)])