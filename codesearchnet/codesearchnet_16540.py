def check_compatible(self, other):
        """Check if *other* can be used in an arithmetic operation.

        1) *other* is a scalar
        2) *other* is a grid defined on the same edges

        :Raises: :exc:`TypeError` if not compatible.
        """
        if not (numpy.isreal(other) or self == other):
            raise TypeError(
                "The argument can not be arithmetically combined with the grid. "
                "It must be a scalar or a grid with identical edges. "
                "Use Grid.resample(other.edges) to make a new grid that is "
                "compatible with other.")
        return True