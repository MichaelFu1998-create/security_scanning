def __update_membership(self):
        """!
        @brief Update membership for each point in line with current cluster centers.

        """
        data_difference = numpy.zeros((len(self.__centers), len(self.__data)))

        for i in range(len(self.__centers)):
            data_difference[i] = numpy.sum(numpy.square(self.__data - self.__centers[i]), axis=1)

        for i in range(len(self.__data)):
            for j in range(len(self.__centers)):
                divider = sum([pow(data_difference[j][i] / data_difference[k][i], self.__degree) for k in range(len(self.__centers)) if data_difference[k][i] != 0.0])

                if divider != 0.0:
                    self.__membership[i][j] = 1.0 / divider
                else:
                    self.__membership[i][j] = 1.0