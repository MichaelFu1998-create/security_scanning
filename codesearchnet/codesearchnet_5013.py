def __create_distance_calculator(self):
        """!
        @brief Creates distance calculator in line with algorithms parameters.

        @return (callable) Distance calculator.

        """
        if self.__data_type == 'points':
            return lambda index1, index2: self.__metric(self.__pointer_data[index1], self.__pointer_data[index2])

        elif self.__data_type == 'distance_matrix':
            if isinstance(self.__pointer_data, numpy.matrix):
                return lambda index1, index2: self.__pointer_data.item((index1, index2))

            return lambda index1, index2: self.__pointer_data[index1][index2]

        else:
            raise TypeError("Unknown type of data is specified '%s'" % self.__data_type)