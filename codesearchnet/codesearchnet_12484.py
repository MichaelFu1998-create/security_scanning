def rgb(self, **kwargs):
        ''' Convert the image to a 3 band RGB for plotting
        
        This method shares the same arguments as plot(). It will perform visual adjustment on the
        image and prepare the data for plotting in MatplotLib. Values are converted to an
        appropriate precision and the axis order is changed to put the band axis last.
        '''

        if "bands" in kwargs:
            use_bands = kwargs["bands"]
            assert len(use_bands) == 3, 'Plot method only supports single or 3-band outputs'
            del kwargs["bands"]
        else:
            use_bands = self._rgb_bands
        if kwargs.get('blm') == True:
            return self.histogram_match(use_bands, **kwargs)
        # if not specified or DRA'ed, default to a 2-98 stretch
        if "histogram" not in kwargs:
            if "stretch" not in kwargs:
                if not self.options.get('dra'):
                    kwargs['stretch'] = [2,98]
            return self.histogram_stretch(use_bands, **kwargs)
        elif kwargs["histogram"] == "equalize":
            return self.histogram_equalize(use_bands, **kwargs)
        elif kwargs["histogram"] == "match":
            return self.histogram_match(use_bands, **kwargs)
        elif kwargs["histogram"] == "minmax":
            return self.histogram_stretch(use_bands, stretch=[0, 100], **kwargs)
        # DRA'ed images should be left alone if not explicitly adjusted
        elif kwargs["histogram"] == "ignore" or self.options.get('dra'):
            data = self._read(self[use_bands,...], **kwargs)
            return np.rollaxis(data, 0, 3)
        else:
            raise KeyError('Unknown histogram parameter, use "equalize", "match", "minmax", or "ignore"')