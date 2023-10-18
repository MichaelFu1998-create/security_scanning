def fugacities(self, xs=None, ys=None):   
        r'''Helper method for calculating fugacity coefficients for any 
        phases present, using either the overall mole fractions for both phases
        or using specified mole fractions for each phase.
        
        Requires `fugacity_coefficients` to be implemented by each subclassing
        EOS.
        
        In addition to setting `fugacities_l` and/or `fugacities_g`, this also
        sets the fugacity coefficients `phis_l` and/or `phis_g`.
        
        .. math::
            \hat \phi_i^g = \frac{\hat f_i^g}{x_i P}
        
            \hat \phi_i^l = \frac{\hat f_i^l}{x_i P}
        
        Parameters
        ----------
        xs : list[float], optional
            Liquid-phase mole fractions of each species, [-]
        ys : list[float], optional
            Vapor-phase mole fractions of each species, [-]
            
        Notes
        -----
        It is helpful to check that `fugacity_coefficients` has been
        implemented correctly using the following expression, from [1]_.
        
        .. math::
            \ln \hat \phi_i = \left[\frac{\partial (n\log \phi)}{\partial 
            n_i}\right]_{T,P,n_j,V_t}
        
        For reference, several expressions for fugacity of a component are as
        follows, shown in [1]_ and [2]_.
        
        .. math::
             \ln \hat \phi_i = \int_{0}^P\left(\frac{\hat V_i}
             {RT} - \frac{1}{P}\right)dP

             \ln \hat \phi_i = \int_V^\infty \left[
             \frac{1}{RT}\frac{\partial P}{ \partial n_i}
             - \frac{1}{V}\right] d V - \ln Z
             
        References
        ----------
        .. [1] Hu, Jiawen, Rong Wang, and Shide Mao. "Some Useful Expressions 
           for Deriving Component Fugacity Coefficients from Mixture Fugacity 
           Coefficient." Fluid Phase Equilibria 268, no. 1-2 (June 25, 2008): 
           7-13. doi:10.1016/j.fluid.2008.03.007.
        .. [2] Walas, Stanley M. Phase Equilibria in Chemical Engineering. 
           Butterworth-Heinemann, 1985.
        '''
        if self.phase in ['l', 'l/g']:
            if xs is None:
                xs = self.zs
            self.phis_l = self.fugacity_coefficients(self.Z_l, zs=xs)
            self.fugacities_l = [phi*x*self.P for phi, x in zip(self.phis_l, xs)]
            self.lnphis_l = [log(i) for i in self.phis_l]
        if self.phase in ['g', 'l/g']:
            if ys is None:
                ys = self.zs
            self.phis_g = self.fugacity_coefficients(self.Z_g, zs=ys)
            self.fugacities_g = [phi*y*self.P for phi, y in zip(self.phis_g, ys)]
            self.lnphis_g = [log(i) for i in self.phis_g]