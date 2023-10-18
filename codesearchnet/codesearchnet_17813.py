def contour(self, level):
        """Get contour lines at the given level.

        Parameters
        ----------
        level : numbers.Number
            The data level to calculate the contour lines for.

        Returns
        -------
        :
            The result of the :attr:`formatter` called on the contour at the
            given `level`.

        """
        if not isinstance(level, numbers.Number):
            raise TypeError(
                ("'_level' must be of type 'numbers.Number' but is "
                 "'{:s}'").format(type(level)))
        vertices = self._contour_generator.create_contour(level)
        return self.formatter(level, vertices)