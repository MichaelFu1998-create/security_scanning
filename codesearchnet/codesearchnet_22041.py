def imgmax(self):
        """
        Highest value of input image.
        """
        if not hasattr(self, '_imgmax'):
            imgmax = _np.max(self.images[0])
            for img in self.images:
                imax = _np.max(img)
                if imax > imgmax:
                    imgmax = imax

            self._imgmax = imgmax

        return self._imgmax