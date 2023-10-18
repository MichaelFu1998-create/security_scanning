def __calculate_changes(self, updated_centers):
        """!
        @brief Calculate changes between centers.

        @return (float) Maximum change between centers.

        """
        changes = numpy.sum(numpy.square(self.__centers - updated_centers), axis=1).T
        return numpy.max(changes)