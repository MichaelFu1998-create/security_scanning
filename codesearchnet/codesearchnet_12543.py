def window_cover(self, window_shape, pad=True):
        """ Iterate over a grid of windows of a specified shape covering an image.

        The image is divided into a grid of tiles of size window_shape. Each iteration returns
        the next window.


        Args:
            window_shape (tuple): The desired shape of each image as (height,
                width) in pixels.
            pad: (bool): Whether or not to pad edge cells. If False, cells that do not
                have the desired shape will not be returned. Defaults to True.

        Yields:
            image: image object of same type.
        """
        size_y, size_x = window_shape[0], window_shape[1]
        _ndepth, _nheight, _nwidth = self.shape
        nheight, _m = divmod(_nheight, size_y)
        nwidth, _n = divmod(_nwidth, size_x)

        img = self
        if pad is True:
            new_height, new_width = _nheight, _nwidth
            if _m != 0:
                new_height = (nheight + 1) * size_y
            if _n != 0:
                new_width = (nwidth + 1) * size_x
            if (new_height, new_width) != (_nheight, _nwidth):
                bounds = box(0, 0, new_width, new_height)
                geom = ops.transform(self.__geo_transform__.fwd, bounds)
                img = self[geom]

        row_lims = range(0, img.shape[1], size_y)
        col_lims = range(0, img.shape[2], size_x)
        for maxy, maxx in product(row_lims, col_lims):
            reg = img[:, maxy:(maxy + size_y), maxx:(maxx + size_x)]
            if pad is False:
                if reg.shape[1:] == window_shape:
                    yield reg
            else:
                yield reg