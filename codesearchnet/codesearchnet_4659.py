def __read_answer(self):
        """!
        @brief Read information about proper clusters and noises from the file.

        """

        if self.__clusters is not None:
            return

        file = open(self.__answer_path, 'r')

        self.__clusters, self.__noise = [], []

        index_point = 0
        for line in file:
            self.__read_answer_from_line(index_point, line)
            index_point += 1

        file.close()