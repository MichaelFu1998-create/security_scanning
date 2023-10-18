def __process_by_python(self):
        """!
        @brief Performs processing using python code.

        """
        for index_cluster in range(len(self.__clusters)):
            for index_point in self.__clusters[index_cluster]:
                self.__score[index_point] = self.__calculate_score(index_point, index_cluster)