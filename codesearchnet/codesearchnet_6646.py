def _coeff_ind_from_T(self, T):
        '''Determines the index at which the coefficients for the current
        temperature are stored in `coeff_sets`.
        '''
        # DO NOT CHANGE
        if self.n == 1:
            return 0
        for i in range(self.n):
            if T <= self.Ts[i+1]:
                return i
        return self.n - 1