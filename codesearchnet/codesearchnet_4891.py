def __calculate_volume(self):
        """!
        @brief Calculates volume of current spatial block.
        @details If empty dimension is detected (where all points has the same value) then such dimension is ignored
                  during calculation of volume.

        @return (double) Volume of current spatial block.

        """

        volume = 0.0
        for i in range(0, len(self.__max_corner)):
            side_length = self.__max_corner[i] - self.__min_corner[i]

            if side_length != 0.0:
                if volume == 0.0: volume = side_length
                else: volume *= side_length

        return volume