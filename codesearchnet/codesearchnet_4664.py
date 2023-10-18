def __create_pairs(self, dimension, acceptable_pairs):
        """!
        @brief Create coordinate pairs that should be displayed.

        @param[in] dimension (uint): Data-space dimension.
        @param[in] acceptable_pairs (list): List of coordinate pairs that should be displayed.

        @return (list) List of coordinate pairs that should be displayed.

        """
        if len(acceptable_pairs) > 0:
            return acceptable_pairs

        return list(itertools.combinations(range(dimension), 2))