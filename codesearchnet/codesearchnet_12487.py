def histogram_stretch(self, use_bands, **kwargs):
        ''' entry point for contrast stretching '''
        data = self._read(self[use_bands,...], **kwargs)
        data = np.rollaxis(data.astype(np.float32), 0, 3)
        return self._histogram_stretch(data, **kwargs)