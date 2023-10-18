def initialize(self, **kwargs):
        """!
        @brief Calculates initial centers using K-Means++ method.

        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'return_index').

        <b>Keyword Args:</b><br>
            - return_index (bool): If True then returns indexes of points from input data instead of points itself.

        @return (list) List of initialized initial centers.
                  If argument 'return_index' is False then returns list of points.
                  If argument 'return_index' is True then returns list of indexes.
        
        """

        return_index = kwargs.get('return_index', False)

        index_point = self.__get_initial_center(True)
        centers = [index_point]
        self.__free_indexes.remove(index_point)

        # For each next center
        for _ in range(1, self.__amount):
            index_point = self.__get_next_center(centers, True)
            centers.append(index_point)
            self.__free_indexes.remove(index_point)

        if not return_index:
            centers = [self.__data[index] for index in centers]

        return centers