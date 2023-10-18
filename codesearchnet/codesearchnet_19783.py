def model_uncert(self):
        """
        Estimate the photometric uncertainties on each data point following Equation A.2 of The Paper.
        Based on the kepcal package of Dan Foreman-Mackey.
        """
        Y = self.photometry_array.T
        Y /= np.median(Y, axis=1)[:, None]
        C = np.median(Y, axis=0)
        
        nstars, nobs = np.shape(Y)
        
        Z = np.empty((nstars, 4))
        
        qs = self.qs.astype(int)
        
        for s in range(4):
            Z[:, s] = np.median((Y / C)[:, qs == s], axis=1)

        resid2 = (Y - Z[:, qs] * C)**2
        z = Z[:, qs]
        trend = z * C[None, :]
        
        lnS = np.log(np.nanmedian(resid2, axis=0))
        jitter = np.log(0.1*np.nanmedian(np.abs(np.diff(Y, axis=1))))

        cal_ferr = np.sqrt(np.exp(2*(jitter/trend))+z**2*np.exp(lnS)[None, :])
        
        self.modeled_uncert = cal_ferr
        self.target_uncert = cal_ferr[0]