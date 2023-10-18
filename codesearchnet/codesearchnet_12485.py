def histogram_equalize(self, use_bands, **kwargs):
        ''' Equalize and the histogram and normalize value range
            Equalization is on all three bands, not per-band'''
        data = self._read(self[use_bands,...], **kwargs)
        data = np.rollaxis(data.astype(np.float32), 0, 3)
        flattened = data.flatten()
        if 0 in data:
            masked = np.ma.masked_values(data, 0).compressed()
            image_histogram, bin_edges = np.histogram(masked, 256)
        else:
            image_histogram, bin_edges = np.histogram(flattened, 256)
        bins = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        cdf = image_histogram.cumsum() 
        cdf = cdf / float(cdf[-1])
        image_equalized = np.interp(flattened, bins, cdf).reshape(data.shape)
        if 'stretch' in kwargs or 'gamma' in kwargs:
            return self._histogram_stretch(image_equalized, **kwargs)
        else:
            return image_equalized