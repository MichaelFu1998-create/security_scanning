def __get_next_center(self, centers, return_index):
        """!
        @brief Calculates the next center for the data.

        @param[in] centers (array_like): Current initialized centers.
        @param[in] return_index (bool): If True then return center's index instead of point.

        @return (array_like) Next initialized center.<br>
                (uint) Index of next initialized center if return_index is True.

        """

        distances = self.__calculate_shortest_distances(self.__data, centers, return_index)

        if self.__candidates == kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE:
            center_index = numpy.nanargmax(distances)
        else:
            probabilities = self.__calculate_probabilities(distances)
            center_index = self.__get_probable_center(distances, probabilities)

        if return_index:
            return center_index

        return self.__data[center_index]