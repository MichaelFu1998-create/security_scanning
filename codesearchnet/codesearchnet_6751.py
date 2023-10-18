def solve(self):
        '''First EOS-generic method; should be called by all specific EOSs.
        For solving for `T`, the EOS must provide the method `solve_T`.
        For all cases, the EOS must provide `a_alpha_and_derivatives`.
        Calls `set_from_PT` once done.
        '''
        self.check_sufficient_inputs()
        
        if self.V:
            if self.P:
                self.T = self.solve_T(self.P, self.V)
                self.a_alpha, self.da_alpha_dT, self.d2a_alpha_dT2 = self.a_alpha_and_derivatives(self.T)
            else:
                self.a_alpha, self.da_alpha_dT, self.d2a_alpha_dT2 = self.a_alpha_and_derivatives(self.T)
                self.P = R*self.T/(self.V-self.b) - self.a_alpha/(self.V*self.V + self.delta*self.V + self.epsilon)
            Vs = [self.V, 1j, 1j]
        else:
            self.a_alpha, self.da_alpha_dT, self.d2a_alpha_dT2 = self.a_alpha_and_derivatives(self.T)
            Vs = self.volume_solutions(self.T, self.P, self.b, self.delta, self.epsilon, self.a_alpha)
        self.set_from_PT(Vs)