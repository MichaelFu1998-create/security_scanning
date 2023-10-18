def __process_by_ccore(self):
        """!
        @brief Performs processing using CCORE (C/C++ part of pyclustering library).

        """
        ccore_metric = metric_wrapper.create_instance(self.__metric)
        self.__score = wrapper.silhoeutte(self.__data, self.__clusters, ccore_metric.get_pointer())