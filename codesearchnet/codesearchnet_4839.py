def capture_points(self, data, point_availability):
        """!
        @brief Finds points that belong to this block using availability map to reduce computational complexity by
                checking whether the point belongs to the block.
        @details Algorithm complexity of this method is O(n).

        @param[in] data (array_like): Data where points are represented as coordinates.
        @param[in] point_availability (array_like): Contains boolean values that denote whether point is already belong
                    to another CLIQUE block.

        """
        for index_point in range(len(data)):
            if (point_availability[index_point] is True) and (data[index_point] in self.__spatial_location):
                self.__points.append(index_point)
                point_availability[index_point] = False