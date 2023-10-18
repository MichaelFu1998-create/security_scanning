def __calculate_dataset_difference(self, index_point):
        """!
        @brief Calculate distance from each object to specified object.

        @param[in] index_point (uint): Index point for which difference with other points is calculated.

        @return (list) Distance to each object from input data from the specified.

        """

        if self.__metric.get_type() != type_metric.USER_DEFINED:
            dataset_differences = self.__metric(self.__data, self.__data[index_point])
        else:
            dataset_differences = [self.__metric(point, self.__data[index_point]) for point in self.__data]

        return dataset_differences