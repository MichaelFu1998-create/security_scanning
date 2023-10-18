def set_shape(self, shape, inner):
        """
        Set the overall shape of the calculation area. The total shape of that
        the calculation can possibly occupy, in pixels. The second, inner, is
        the region of interest within the image.
        """
        if self.shape != shape or self.inner != inner:
            self.shape = shape
            self.inner = inner
            self.initialize()