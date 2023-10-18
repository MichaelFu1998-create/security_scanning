def set_mem_level(self, mem_level='hi'):
        """
        Sets the memory usage level of the state.

        Parameters
        ----------
        mem_level : string
            Can be set to one of:
                * hi      : all mem's are np.float64
                * med-hi  : image, platonic are float32, rest are float64
                * med     : all mem's are float32
                * med-lo  : image, platonic are float16, rest float32
                * lo      : all are float16, which is bad for accuracy.

        Notes
        -----
        Right now the PSF is not affected by the mem-level changes, which is
        OK for mem but it means that self._model, self._residuals are always
        float64, which can be a chunk of mem.
        """
        #A little thing to parse strings for convenience:
        key = ''.join([c if c in 'mlh' else '' for c in mem_level])
        if key not in ['h','mh','m','ml','m', 'l']:
            raise ValueError('mem_level must be one of hi, med-hi, med, med-lo, lo.')
        mem_levels = {  'h':     [np.float64, np.float64],
                        'mh': [np.float64, np.float32],
                        'm':   [np.float32, np.float32],
                        'ml':  [np.float32, np.float16],
                        'l':      [np.float16, np.float16]
                    }
        hi_lvl, lo_lvl = mem_levels[key]
        cat_lvls = {'obj':lo_lvl,
                    'ilm':hi_lvl,
                    'bkg':lo_lvl
                    }  #no psf...

        self.image.float_precision = hi_lvl
        self.image.image = self.image.image.astype(lo_lvl)
        self.set_image(self.image)

        for cat in cat_lvls.keys():
            obj = self.get(cat)
            #check if it's a component collection
            if hasattr(obj, 'comps'):
                for c in obj.comps:
                    c.float_precision = lo_lvl
            else:
                obj.float_precision = lo_lvl
        self._model = self._model.astype(hi_lvl)
        self._residuals = self._model.astype(hi_lvl)
        self.reset()