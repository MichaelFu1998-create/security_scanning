def process(self):
        """!
        @brief Performs cluster analysis in line with Fuzzy C-Means algorithm.

        @see get_clusters()
        @see get_centers()
        @see get_membership()

        """
        if self.__ccore is True:
            self.__process_by_ccore()
        else:
            self.__process_by_python()

        return self