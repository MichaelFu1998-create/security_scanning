def zoom_region(self):
        """The zoomed rectangular region corresponding to the square encompassing all unmasked values.

        This is used to zoom in on the region of an image that is used in an analysis for visualization."""

        # Have to convert mask to bool for invert function to work.
        where = np.array(np.where(np.invert(self.astype('bool'))))
        y0, x0 = np.amin(where, axis=1)
        y1, x1 = np.amax(where, axis=1)
        return [y0, y1+1, x0, x1+1]