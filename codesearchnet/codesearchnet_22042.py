def imgmin(self):
        """
        Lowest value of input image.
        """
        if not hasattr(self, '_imgmin'):
            imgmin = _np.min(self.images[0])
            for img in self.images:
                imin = _np.min(img)
                if imin > imgmin:
                    imgmin = imin

            self._imgmin = imgmin
        return _np.min(self.image)