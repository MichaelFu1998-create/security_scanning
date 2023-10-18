def __cache_covered_data(self):
        """!
        @brief Cache covered data.

        """
        self.__cache_points = True
        self.__points = []

        for index_point in range(len(self.__data)):
            if self.__data[index_point] in self.__spatial_block:
                self.__cache_point(index_point)