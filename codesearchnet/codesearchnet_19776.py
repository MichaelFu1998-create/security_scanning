def do_photometry(self):
        """
        Does photometry and estimates uncertainties by calculating the scatter around a linear fit to the data
        in each orientation. This function is called by other functions and generally the user will not need
        to interact with it directly.
        """
        
        std_f = np.zeros(4)
        data_save = np.zeros_like(self.postcard)
        self.obs_flux = np.zeros_like(self.reference_flux)


        for i in range(4):
            g = np.where(self.qs == i)[0]
            wh = np.where(self.times[g] > 54947)

            data_save[g] = np.roll(self.postcard[g], int(self.roll_best[i,0]), axis=1)
            data_save[g] = np.roll(data_save[g], int(self.roll_best[i,1]), axis=2)

            self.target_flux_pixels = data_save[:,self.targets == 1]
            self.target_flux = np.sum(self.target_flux_pixels, axis=1)
            
            self.obs_flux[g] = self.target_flux[g] / self.reference_flux[g]
            self.obs_flux[g] /= np.median(self.obs_flux[g[wh]])
            
            fitline = np.polyfit(self.times[g][wh], self.obs_flux[g][wh], 1)
            std_f[i] = np.max([np.std(self.obs_flux[g][wh]/(fitline[0]*self.times[g][wh]+fitline[1])), 0.001])
        
        self.flux_uncert = std_f