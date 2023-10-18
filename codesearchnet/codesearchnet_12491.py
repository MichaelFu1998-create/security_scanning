def plot(self, spec="rgb", **kwargs):
        ''' Plot the image with MatplotLib

        Plot sizing includes default borders and spacing. If the image is shown in Jupyter the outside whitespace will be automatically cropped to save size, resulting in a smaller sized image than expected.

        Histogram options:
            * 'equalize': performs histogram equalization on the image.
            * 'minmax': stretch the pixel range to the minimum and maximum input pixel values. Equivalent to stretch=[0,100].
            * 'match': match the histogram to the Maps API imagery. Pass the additional keyword blm_source='browse' to match to the Browse Service (image thumbnail) instead.
            * 'ignore': Skip dynamic range adjustment, in the event the image is already correctly balanced and the values are in the correct range.
            
        Gamma values greater than 1 will brighten the image midtones, values less than 1 will darken the midtones.

        Plots generated with the histogram options of 'match' and 'equalize' can be combined with the stretch and gamma options. The stretch and gamma adjustments will be applied after the histogram adjustments.
        
        Args:
            w (float or int): width of plot in inches at 72 dpi, default is 10
            h (float or int): height of plot in inches at 72 dpi, default is 10
            title (str): Title to use on the plot
            fontsize (int): Size of title font, default is 22. Size is measured in points.
            bands (list): bands to use for plotting, such as bands=[4,2,1]. Defaults to the image's natural RGB bands. This option is useful for generating pseudocolor images when passed a list of three bands. If only a single band is provided, a colormapped plot will be generated instead.
            cmap (str): MatPlotLib colormap name to use for single band images. Default is colormap='Grey_R'.
            histogram (str): either 'equalize', 'minmax', 'match', or ignore
            stretch (list): stretch the histogram between two percentile values, default is [2,98]
            gamma (float): adjust image gamma, default is 1.0
        '''

        if self.shape[0] == 1 or ("bands" in kwargs and len(kwargs["bands"]) == 1):
            if "cmap" in kwargs:
                cmap = kwargs["cmap"]
                del kwargs["cmap"]
            else:
                cmap = "Greys_r"
            self._plot(tfm=self._single_band, cmap=cmap, **kwargs)
        else:
            if spec == "rgb" and self._has_token(**kwargs):
                self._plot(tfm=self.rgb, **kwargs)
            else:
                self._plot(tfm=getattr(self, spec), **kwargs)