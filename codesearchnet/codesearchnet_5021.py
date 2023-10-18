def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using CCORE (C/C++ part of pyclustering library).

        """
        cure_data_pointer = wrapper.cure_algorithm(self.__pointer_data, self.__number_cluster,
                                                   self.__number_represent_points, self.__compression)

        self.__clusters = wrapper.cure_get_clusters(cure_data_pointer)
        self.__representors = wrapper.cure_get_representors(cure_data_pointer)
        self.__means = wrapper.cure_get_means(cure_data_pointer)

        wrapper.cure_data_destroy(cure_data_pointer)