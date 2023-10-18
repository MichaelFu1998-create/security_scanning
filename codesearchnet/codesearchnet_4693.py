def __create_distance_calculator_basic(self):
        """!
        @brief Creates distance metric calculator that does not use numpy.

        @return (callable) Callable object of distance metric calculator.

        """
        if self.__type == type_metric.EUCLIDEAN:
            return euclidean_distance

        elif self.__type == type_metric.EUCLIDEAN_SQUARE:
            return euclidean_distance_square

        elif self.__type == type_metric.MANHATTAN:
            return manhattan_distance

        elif self.__type == type_metric.CHEBYSHEV:
            return chebyshev_distance

        elif self.__type == type_metric.MINKOWSKI:
            return lambda point1, point2: minkowski_distance(point1, point2, self.__args.get('degree', 2))

        elif self.__type == type_metric.CANBERRA:
            return canberra_distance

        elif self.__type == type_metric.CHI_SQUARE:
            return chi_square_distance

        elif self.__type == type_metric.USER_DEFINED:
            return self.__func

        else:
            raise ValueError("Unknown type of metric: '%d'", self.__type)