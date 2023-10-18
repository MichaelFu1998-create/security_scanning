def __calculate_density(self, amount_points):
        """!
        @brief Calculates BANG-block density.

        @param[in] amount_points (uint): Amount of points in block.

        @return (double) BANG-block density.

        """
        volume = self.__spatial_block.get_volume()
        if volume != 0.0:
            return amount_points / volume

        return 0.0