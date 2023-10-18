def __create_point_comparator(self, type_point):
        """!
        @brief Create point comparator.
        @details In case of numpy.array specific comparator is required.

        @param[in] type_point (data_type): Type of point that is stored in KD-node.

        @return (callable) Callable point comparator to compare to points.

        """
        if type_point == numpy.ndarray:
            return lambda obj1, obj2: numpy.array_equal(obj1, obj2)

        return lambda obj1, obj2: obj1 == obj2