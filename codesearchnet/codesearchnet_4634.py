def __process_by_python(self):
        """!
        @brief Performs processing using python implementation.

        """
        for amount in range(self.__kmin, self.__kmax):
            centers = self.__initializer(self.__data, amount).initialize()
            instance = kmeans(self.__data, centers, ccore=True)
            instance.process()

            self.__wce.append(instance.get_total_wce())

        self.__calculate_elbows()
        self.__find_optimal_kvalue()