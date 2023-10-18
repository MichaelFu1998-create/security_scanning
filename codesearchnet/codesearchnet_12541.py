def iterwindows(self, count=64, window_shape=(256, 256)):
        """ Iterate over random windows of an image

        Args:
            count (int): the number of the windows to generate. Defaults to 64, if `None` will continue to iterate over random windows until stopped.
            window_shape (tuple): The desired shape of each image as (height, width) in pixels.

        Yields:
            image: an image of the given shape and same type.
        """
        if count is None:
            while True:
                yield self.randwindow(window_shape)
        else:
            for i in xrange(count):
                yield self.randwindow(window_shape)