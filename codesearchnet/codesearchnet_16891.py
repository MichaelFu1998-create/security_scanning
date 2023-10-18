def rectangle(cls, vertices, **kwargs):
        """Shortcut for creating a rectangle aligned with the screen axes from only two corners.

        Parameters
        ----------
        vertices : array-like
            An array containing the ``[x, y]`` positions of two corners.
        kwargs
            Other keyword arguments are passed to the |Shape| constructor.

        """
        bottom_left, top_right = vertices
        top_left = [bottom_left[0], top_right[1]]
        bottom_right = [top_right[0], bottom_left[1]]
        return cls([bottom_left, bottom_right, top_right, top_left], **kwargs)