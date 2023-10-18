def __calculate_probabilities(self, distances):
        """!
        @brief Calculates cumulative probabilities of being center of each point.

        @param[in] distances (array_like): Distances from each point to closest center.

        @return (array_like) Cumulative probabilities of being center of each point.

        """

        total_distance = numpy.sum(distances)
        if total_distance != 0.0:
            probabilities = distances / total_distance
            return numpy.cumsum(probabilities)
        else:
            return numpy.zeros(len(distances))