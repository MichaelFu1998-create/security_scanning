def __calculate_centers(self):
        """!
        @brief Calculate center using membership of each cluster.

        @return (list) Updated clusters as list of clusters. Each cluster contains indexes of objects from data.

        @return (numpy.array) Updated centers.

        """
        dimension = self.__data.shape[1]
        centers = numpy.zeros((len(self.__centers), dimension))

        for i in range(len(self.__centers)):
            # multiplication '@' requires python version 3.5
            centers[i] = numpy.divide(self.__membership[:, i] @ self.__data, numpy.sum(self.__membership[:, i]))

        return centers