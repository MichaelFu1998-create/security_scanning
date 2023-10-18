def calc_fluxes(self, min_flux = 5000, outlier_iterations=5,
                       max_outlier_obs=4, outlier_limit=1.7):
        """
        Determine the suitable reference stars, and then the total flux in those stars and 
        in the target star in each epoch
        
        Args: 
            min_flux: The size of the region around the target star to be plotted. Images will be a square 
                with side length ``image_region`` (default: ``5000``)
            outlier_iterations: The number of iterations to remove outliers from the reference star sample
                (stars at epochs with more than ``max_outlier_obs`` observations more than ``outlier_limit`` standard
                deviations from the median value for all stars after normalization) (default: ``5``)
            max_outlier_obs: The maximum number of epochs at which a star is allowed to be more than ``outlier_limit``
                standard deviations from the median value for all stars before it is removed as a suitable
                reference star (default: ``4``)
            outlier_limit: The level of deviation (measured in standard deviations) which a target is allowed
                to be discrepant from the median. If it is this discrepant at more than ``max_outlier_obs``
                epochs, it is removed from consideration (default: ``1.7``)
        
        """
        
        jj, ii = self.center
        

        
        numer = np.zeros(len(self.times))
        denom = np.zeros(len(self.times))
        factr = np.zeros(len(self.times))
        
        numer_pix = self.postcard[:,self.targets == 1]
        numer = np.sum(numer_pix, axis=1)
        
        tar_vals = np.zeros((len(self.times), int(np.max(self.targets)+1-2-self.ignore_bright)))
        
        for i in range(2+self.ignore_bright,int(np.max(self.targets)+1)):
            tval = np.sum(self.postcard[:,self.targets == i], axis=1)
            #denom += tval/np.median(tval)
            tar_vals[:,i-2-self.ignore_bright] = tval #/ np.median(tval)
            
        for i in range(len(self.obs_filenames)):
            if np.max(tar_vals[i]) < min_flux:
                tar_vals[self.qs == self.qs[i]] = 0.0

        all_tar = np.zeros((len(self.times), int(np.max(self.targets)-self.ignore_bright)))
        all_tar[:,0] = numer
        all_tar[:,1:] = tar_vals
        
        self.photometry_array = all_tar
        
        for i in range(len(tar_vals[0])):
            for j in range(4):
                g = np.where(self.qs == j)[0]  
                tar_vals[g,i] /= (np.median(tar_vals[g,i])+1e-15)
                

        tar_vals_old = tar_vals + 0.0
    
        for i in range(outlier_iterations):
            nonzeros = np.where(tar_vals[0,:] != 0)[0]
            med = np.median(tar_vals[:,nonzeros], axis=1)
            std = np.std(tar_vals[:,nonzeros], axis=1)

            if np.sum(tar_vals) != 0.0:
                tar_vals_old = tar_vals + 0.0

            for k in range(len(tar_vals[0])):
                h = np.where((np.abs(med-tar_vals[:,k])/std) > outlier_limit)[0]
                if len(h) >= max_outlier_obs:
                    tar_vals[:,k] = 0

        if np.sum(tar_vals) == 0.0:
            tar_vals = tar_vals_old + 0.0

        denom = np.sum(tar_vals, axis=1)
        self.target_flux_pixels = numer_pix
        self.reference_flux = denom