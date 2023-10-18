def __get_initial_center(self, return_index):
        """!
        @brief Choose randomly first center.

        @param[in] return_index (bool): If True then return center's index instead of point.

        @return (array_like) First center.<br>
                (uint) Index of first center.

        """

        index_center = random.randint(0, len(self.__data) - 1)
        if return_index:
            return index_center

        return self.__data[index_center]