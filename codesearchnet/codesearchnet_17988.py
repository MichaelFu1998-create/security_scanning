def set_filter(self, slices, values):
        """
        Sets Fourier-space filters for the image. The image is filtered by
        subtracting values from the image at slices.

        Parameters
        ----------
        slices : List of indices or slice objects.
            The q-values in Fourier space to filter.
        values : np.ndarray
            The complete array of Fourier space peaks to subtract off.  values
            should be the same size as the FFT of the image; only the portions
            of values at slices will be removed.

        Examples
        --------
        To remove a two Fourier peaks in the data at q=(10, 10, 10) &
        (245, 245, 245), where im is the residuals of a model:

            * slices = [(10,10,10), (245, 245, 245)]
            * values = np.fft.fftn(im)
            * im.set_filter(slices, values)
        """
        self.filters = [[sl,values[sl]] for sl in slices]