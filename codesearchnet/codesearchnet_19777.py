def generate_panel(self, img):
        """
        Creates the figure shown in ``adjust_aperture`` for visualization purposes. Called by other functions
        and generally not called by the user directly.

        Args: 
            img: The data frame to be passed through to be plotted. A cutout of the ``integrated_postcard``
        
        """
        plt.figure(figsize=(14,6))
        ax = plt.gca()
        fig = plt.gcf()
        plt.subplot(122)
        
        
        data_save = np.zeros_like(self.postcard)
        self.roll_best = np.zeros((4,2))
        
        for i in range(4):
            g = np.where(self.qs == i)[0]
            wh = np.where(self.times[g] > 54947)

            self.roll_best[i] = self.do_rolltest(g, wh)
            
        self.do_photometry()
        for i in range(4):
            g = np.where(self.qs == i)[0]
            plt.errorbar(self.times[g], self.obs_flux[g], yerr=self.flux_uncert[i], fmt=fmt[i])
            
        plt.xlabel('Time', fontsize=20)
        plt.ylabel('Relative Flux', fontsize=20)
 
        
        plt.subplot(121)
        implot = plt.imshow(img, interpolation='nearest', cmap='gray', vmin=98000*52, vmax=104000*52)
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
        
        plt.show(block=True)