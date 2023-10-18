def _weight(self, rsq, sigma=None):
        """weighting function for Barnes"""
        sigma = sigma or self.filter_size

        if not self.clip:
            o = np.exp(-rsq / (2*sigma**2))
        else:
            o = np.zeros(rsq.shape, dtype='float')
            m = (rsq < self.clipsize**2)
            o[m] = np.exp(-rsq[m] / (2*sigma**2))
        return o