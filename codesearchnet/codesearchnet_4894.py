def __get_amount_points(self):
        """!
        @brief Count covered points by the BANG-block and if cache is enable then covered points are stored.

        @return (uint) Amount of covered points.

        """
        amount = 0
        for index in range(len(self.__data)):
            if self.__data[index] in self.__spatial_block:
                self.__cache_point(index)
                amount += 1

        return amount