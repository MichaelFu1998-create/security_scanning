def __create_distance_calculator_numpy(self):
        """!
        @brief Creates distance metric calculator that uses numpy.

        @return (callable) Callable object of distance metric calculator.

        """
        if self.__type == type_metric.EUCLIDEAN:
            return euclidean_distance_numpy

        elif self.__type == type_metric.EUCLIDEAN_SQUARE:
            return euclidean_distance_square_numpy

        elif self.__type == type_metric.MANHATTAN:
            return manhattan_distance_numpy

        elif self.__type == type_metric.CHEBYSHEV:
            return chebyshev_distance_numpy

        elif self.__type == type_metric.MINKOWSKI:
            return lambda object1, object2: minkowski_distance_numpy(object1, object2, self.__args.get('degree', 2))

        elif self.__type == type_metric.CANBERRA:
            return canberra_distance_numpy

        elif self.__type == type_metric.CHI_SQUARE:
            return chi_square_distance_numpy

        elif self.__type == type_metric.USER_DEFINED:
            return self.__func

        else:
            raise ValueError("Unknown type of metric: '%d'", self.__type)