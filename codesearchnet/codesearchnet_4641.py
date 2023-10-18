def __process_by_python(self):
        """!
        @brief Performs cluster analysis using python code.

        """

        if self.__data_type == 'points':
            self.__kdtree = kdtree(self.__sample_pointer, range(len(self.__sample_pointer)))

        self.__allocate_clusters()

        if (self.__amount_clusters is not None) and (self.__amount_clusters != len(self.get_clusters())):
            analyser = ordering_analyser(self.get_ordering())
            radius, _ = analyser.calculate_connvectivity_radius(self.__amount_clusters)
            if radius is not None:
                self.__eps = radius
                self.__allocate_clusters()