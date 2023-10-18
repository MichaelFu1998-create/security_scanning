def __find_optimal_kvalue(self):
        """!
        @brief Finds elbow and returns corresponding K-value.

        """
        optimal_elbow_value = max(self.__elbows)
        self.__kvalue = self.__elbows.index(optimal_elbow_value) + 1 + self.__kmin