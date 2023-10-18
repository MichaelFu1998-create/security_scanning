def make_postcard(self, npix=300, shape=(1070, 1132), buffer_size=15):
        """
        Develop a "postcard" region around the target star.
        Other stars in this postcard will be used as possible reference stars.
        
        Args: 
            npix: The size of the postcard region. The region will be a square with sides npix pixels
                (default: ``300``)
            shape: The size of each individual image. For Kepler/K2 FFIs this should never need to be
                changed from the default, but will be different for e.g. TESS FFIs (default: ``(1070, 1132)``)
            buffer_size: The number of pixels at the edge of the detector to avoid (default: ``15``)
        """
        
        source = self.kic
        client = kplr.API()
        targ = client.target(source)
        
        channel = [targ.params['Channel_0'], targ.params['Channel_1'], 
                    targ.params['Channel_2'], targ.params['Channel_3']]

        col = [targ.params['Column_0'], targ.params['Column_1'], 
                    targ.params['Column_2'], targ.params['Column_3']] 

        row = [targ.params['Row_0'], targ.params['Row_1'], 
                    targ.params['Row_2'], targ.params['Row_3']] 
        

        if None in row:
            raise ValueError('Star not on detector all quarters!')

        if None in col:
            raise ValueError('Star not on detector all quarters!')
            
        center = np.array([npix/2, npix/2])
        
        
        # If star close to edge, shift frame so that we have the full npix by npix
        # In this case, postcard will not be centered on target star
        if (np.min(col) < npix/2):
            jump = npix/2 - np.min(col) + buffer_size
            col += jump
            center[1] -= jump
            
        if (np.min(row) < npix/2):
            jump = npix/2 - np.min(row) + buffer_size
            row += jump
            center[0] -= jump
            
        if (np.max(row) > shape[0] - npix/2):
            jump = shape[0]-npix/2 - np.max(row) - buffer_size
            row += jump
            center[0] -= jump
            
        if (np.max(col) > shape[1] - npix/2):
            jump = shape[1]-npix/2 - np.max(col) - buffer_size
            col += jump
            center[1] -= jump
        
        fin_arr = np.zeros((len(self.times), npix, npix))

        for icount, iname in enumerate(self.obs_filenames): 
            a = fits.open(self.ffi_dir+iname)

                        
            quarter = a[0].header['quarter']

            if int(quarter) == 0:
                season = 3
            else:
                season = (int(quarter) - 2) % 4

            #season_arr[icount] = season
            img = a[channel[season]].data
            img -= np.median(img)
            
            
            ymin = int(max([int(row[season])-npix/2,0]))
            ymax = int(min([int(row[season])+npix/2,img.shape[0]]))
            xmin = int(max([int(col[season])-npix/2,0]))
            xmax = int(min([int(col[season])+npix/2,img.shape[1]]))

            pimg = img[ymin:ymax,xmin:xmax]
            fin_arr[icount,:,:] = pimg
        
        self.postcard = fin_arr
        self.integrated_postcard = np.sum(self.postcard, axis=0)
        self.center = center