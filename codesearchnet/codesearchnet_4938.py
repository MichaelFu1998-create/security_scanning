def __create_center(self, return_index):
        """!
        @brief Generates and returns random center.

        @param[in] return_index (bool): If True then returns index of point from input data instead of point itself.
        
        """
        random_index_point = random.randint(0, len(self.__data[0]))
        if random_index_point not in self.__available_indexes:
            random_index_point = self.__available_indexes.pop()
        else:
            self.__available_indexes.remove(random_index_point)

        if return_index:
            return random_index_point
        return self.__data[random_index_point]