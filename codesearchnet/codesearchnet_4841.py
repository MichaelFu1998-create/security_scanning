def increment(self):
        """!
        @brief Forms logical location for next block.

        """
        for index_dimension in range(self.__dimension):
            if self.__coordiate[index_dimension] + 1 < self.__intervals:
                self.__coordiate[index_dimension] += 1
                return
            else:
                self.__coordiate[index_dimension] = 0

        self.__coordiate = None