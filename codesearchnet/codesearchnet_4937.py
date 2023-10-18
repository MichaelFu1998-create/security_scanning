def initialize(self, **kwargs):
        """!
        @brief Generates random centers in line with input parameters.

        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'return_index').

        <b>Keyword Args:</b><br>
            - return_index (bool): If True then returns indexes of points from input data instead of points itself.

        @return (list) List of initialized initial centers.
                  If argument 'return_index' is False then returns list of points.
                  If argument 'return_index' is True then returns list of indexes.
        
        """
        return_index = kwargs.get('return_index', False)
        if self.__amount == len(self.__data):
            if return_index:
                return list(range(len(self.__data)))
            return self.__data[:]

        return [self.__create_center(return_index) for _ in range(self.__amount)]