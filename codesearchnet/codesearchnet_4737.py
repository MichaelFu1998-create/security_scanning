def __process_by_python(self):
        """!
        @brief Performs cluster analysis using Python implementation.

        """
        self.__data = numpy.array(self.__data)
        self.__centers = numpy.array(self.__centers)

        self.__membership = numpy.zeros((len(self.__data), len(self.__centers)))

        change = float('inf')
        iteration = 0

        while change > self.__tolerance and iteration < self.__itermax:
            self.__update_membership()
            centers = self.__calculate_centers()
            change = self.__calculate_changes(centers)

            self.__centers = centers
            iteration += 1

        self.__extract_clusters()