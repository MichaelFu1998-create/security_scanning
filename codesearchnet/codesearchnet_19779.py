def data_for_target(self, do_roll=True, ignore_bright=0):
        """
        Determine the normalized photometry, accounting for effects shared by reference stars. Does not provide
        the opportunity to adjust the aperture
        
        Args: 
            image_region: If ``True`` allow the aperture to be shifted up to one pixel in both the x and y
                directions to account for differential velocity aberration (default: ``True``)
            ignore_bright: The number of brightest stars to be ignored in the determination of the flux from 
                reference stars. If there is reason to believe (for example) that saturated stars may behave
                differently than the target star, they can be avoided with this flag (default: ``0``)
        
        """
        self.ignore_bright = ignore_bright
        self.calc_fluxes()
        self.roll_best = np.zeros((4,2))

        
        if do_roll == True:
            for i in range(4):
                g = np.where(self.qs == i)[0]
                wh = np.where(self.times[g] > 54947)

                self.roll_best[i] = self.do_rolltest(g, wh)
                
        self.do_photometry()