def randwindow(self, window_shape):
        """Get a random window of a given shape from within an image

        Args:
            window_shape (tuple): The desired shape of the returned image as (height, width) in pixels.

        Returns:
            image: a new image object of the specified shape and same type
        """
        row = random.randrange(window_shape[0], self.shape[1])
        col = random.randrange(window_shape[1], self.shape[2])
        return self[:, row-window_shape[0]:row, col-window_shape[1]:col]