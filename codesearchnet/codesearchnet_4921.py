def __process_by_ccore(self):
        """!
        @brief Performs processing using CCORE (C/C++ part of pyclustering library).

        """
        results = wrapper.silhoeutte_ksearch(self.__data, self.__kmin, self.__kmax, self.__algorithm)

        self.__amount = results[0]
        self.__score = results[1]
        self.__scores = results[2]