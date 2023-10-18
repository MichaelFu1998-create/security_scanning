def __cache_point(self, index):
        """!
        @brief Store index points.

        @param[in] index (uint): Index point that should be stored.

        """
        if self.__cache_points:
            if self.__points is None:
                self.__points = []

            self.__points.append(index)