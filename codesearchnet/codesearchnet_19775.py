def find_other_sources(self,  edge_lim = 0.015, min_val = 5000, 
                          ntargets = 250, extend_region_size=3, remove_excess=4,
                          plot_flag = False, plot_window=15):
        """
        Identify apertures for all sources on the postcard, both for the 
        target and potential reference stars
        
        Args: 
            edge_lim: The initial limit for the creation of apertures. The aperture will be a region of
                contiguous pixels with flux values larger than the product of ``edge_lim`` and the brightest
                pixel value for this star, as long as that product is larger than ``min_val`` (default: ``0.015``)
            min_val: Threshold for the minimum flux value in the ``integrated_postcard`` for a pixel to be included 
                in the default apertures (default: ``5000``)
            ntargets: The maximum number of potential reference stars to be included in the analysis (default: ``250``)
            extend_region_size: After the initial apertures are generated, they will be optionally extended an
                additional number of pixels following this flag. Safe practice for reasonable apertures is to 
                leave ``min_val`` at a value well above the noise and then extend apertures via this flag until 
                they are of suitable size (default: ``3``)
            remove_excess: Stars with apertures that touch will be combined into a single aperture. 
                This is done by iterating through the starlist; this flag represents the number of times the
                list will be iterated through to delete redundant apertures (default: ``4``)
            plot_flag: If true, a series of diagnostic plots will appear while this function runs to observe
                apertures for the target star and other stars.
                (default: ``False``)
            plot_window: If ``plot_flag`` is ``True``, the size of the region to be plotted around the target star
                to show the drawn aperture for visualization purposes only (default: ``15``)
        
        """
        j,i = self.center
        
        region = self.integrated_postcard + 0.0
        if plot_flag == True:
            ff = plt.imshow(self.integrated_postcard, interpolation='nearest', cmap='gray', 
                            vmax = np.percentile(region, 99.6))
            plt.colorbar(ff)
            plt.show()
        targets = np.zeros_like(self.integrated_postcard)
        sizeimg = np.shape(targets)[0]
        
        jj = j + 0
        ii = i + 0
        
        edge = edge_lim
        
        lim = max(min_val, self.integrated_postcard[int(j), int(i)]*edge)
        
        maxpt = np.percentile(self.integrated_postcard, 94)
        
        bin_img = (region > lim)
        lab_img, n_features = label(bin_img)
        
        key_targ = (lab_img == (lab_img[int(j), int(i)]))
        tot = np.sum(key_targ)
    
        targets[key_targ] = 1
        region[key_targ] = 0.0
        

        
        lim = np.zeros(ntargets)
        for peaks in range(1,ntargets):
            k = np.argmax(region)
            j,i = np.unravel_index(k, region.shape)
            lim[peaks] = max(maxpt, edge*region[j,i])


            bin_img = (region >= lim[peaks])
            lab_img, n_features = label(bin_img)

            key_targ = (lab_img == (lab_img[j,i]))
            targets[key_targ] = peaks + 1
            region[key_targ] = 0.0
        
        lab_img, n_features = label(targets)
        for i in range(1, ntargets+1):
            for j in range(extend_region_size):
                border= mh.labeled.border(targets, 0, i)

                targets[border*(region < (10)*lim[peaks])] = i
        for i in range(2, ntargets+1):
            for j in range(2, ntargets+1):
                if i != j:
                    border = mh.labeled.border(targets, i, j)
                    if np.sum(border) != 0:
                        targets[targets == j] = i
    
        targets = mh.labeled.remove_bordering(targets)
        for k in range(remove_excess):
            for i in range(ntargets):
                if np.sum(self.integrated_postcard[targets == i]) < 0.01:
                    targets[targets > i] -= 1

        self.targets = targets
        
        if plot_flag == True:
            plt.imshow(self.targets, interpolation='nearest')
            plt.show()

            plt.imshow(((targets == 1)*self.integrated_postcard + (targets == 1)*100000)
                       [jj-plot_window:jj+plot_window,ii-plot_window:ii+plot_window], 
                       interpolation='nearest', cmap='gray', vmax=np.percentile(self.integrated_postcard, 99.6))
            plt.show()

            plt.imshow((np.ceil(targets/100.0)*self.integrated_postcard+np.ceil(targets/500.0)*3500000), 
                       interpolation='nearest', cmap='gray', vmax=np.percentile(self.integrated_postcard, 99.99))
            plt.show()