def adjust_aperture(self, image_region=15, ignore_bright=0):
        """
        Develop a panel showing the current aperture and the light curve as judged from that aperture.
        Clicking on individual pixels on the aperture will toggle those pixels on or off into the
        aperture (which will be updated after closing the plot).
        Clicking on the 0th row or column will turn off all pixels in that column or row, respectively.
        Will iterate continuously until the figure is closed without updating any pixels.
        

        Args: 
            image_region: The size of the region around the target star to be plotted. Images will be a square 
                with side length ``image_region`` (default: ``15``)
            ignore_bright: The number of brightest stars to be ignored in the determination of the flux from 
                reference stars. If there is reason to believe (for example) that saturated stars may behave
                differently than the target star, they can be avoided with this flag (default: ``0``)
        
        """
        self.ignore_bright = ignore_bright
        self.calc_fluxes()
        
        self.coordsx = []
        self.coordsy = []
        
        jj, ii = self.center
        jj, ii = int(jj), int(ii)  # Indices must be integer
        plt.ion()
        img = np.sum(((self.targets == 1)*self.postcard + (self.targets == 1)*100000)
                     [:,jj-image_region:jj+image_region,ii-image_region:ii+image_region], axis=0)
        self.generate_panel(img)
        
        while len(self.coordsx) != 0:
            for i in range(len(self.coordsx)):
                if self.targets[self.coordsy[i]+jj-image_region,self.coordsx[i]+ii-image_region] != 1:
                    self.targets[self.coordsy[i]+jj-image_region,self.coordsx[i]+ii-image_region] = 1
                elif self.targets[self.coordsy[i]+jj-image_region,self.coordsx[i]+ii-image_region] == 1:
                    self.targets[self.coordsy[i]+jj-image_region,self.coordsx[i]+ii-image_region] = 0
                if self.coordsy[i] == 0:
                    thiscol = np.where(self.targets[:,self.coordsx[i]+ii-image_region] == 1)
                    self.targets[thiscol,self.coordsx[i]+ii-image_region] = 0
                if self.coordsx[i] == 0:
                    thiscol = np.where(self.targets[self.coordsy[i]+jj-image_region,:] == 1)
                    self.targets[self.coordsy[i]+jj-image_region, thiscol] = 0


            self.coordsx = []
            self.coordsy = []
            img = np.sum(((self.targets == 1)*self.postcard + 
                          (self.targets == 1)*100000)[:,jj-image_region:jj+image_region,ii-image_region:ii+image_region],
                         axis=0)
            self.generate_panel(img)