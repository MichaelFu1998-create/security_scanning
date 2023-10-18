def process(self):
        """!
        @brief Performs clustering process in line with rules of BANG clustering algorithm.

        @return (bang) Returns itself (BANG instance).

        @see get_clusters()
        @see get_noise()
        @see get_directory()
        @see get_dendrogram()

        """
        self.__directory = bang_directory(self.__data, self.__levels,
                                          density_threshold=self.__density_threshold,
                                          amount_threshold=self.__amount_threshold)
        self.__allocate_clusters()

        return self