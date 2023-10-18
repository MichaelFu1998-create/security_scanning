def enable_numpy_usage(self):
        """!
        @brief Start numpy for distance calculation.
        @details Useful in case matrices to increase performance. No effect in case of type_metric.USER_DEFINED type.

        """
        self.__numpy = True
        if self.__type != type_metric.USER_DEFINED:
            self.__calculator = self.__create_distance_calculator()