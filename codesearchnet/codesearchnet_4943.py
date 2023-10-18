def __get_probable_center(self, distances, probabilities):
        """!
        @brief Calculates the next probable center considering amount candidates.

        @param[in] distances (array_like): Distances from each point to closest center.
        @param[in] probabilities (array_like): Cumulative probabilities of being center of each point.

        @return (uint) Index point that is next initialized center.

        """

        index_best_candidate = -1
        for _ in range(self.__candidates):
            candidate_probability = random.random()
            index_candidate = 0

            for index_object in range(len(probabilities)):
                if candidate_probability < probabilities[index_object]:
                    index_candidate = index_object
                    break

            if index_best_candidate == -1:
                index_best_candidate = next(iter(self.__free_indexes))
            elif distances[index_best_candidate] < distances[index_candidate]:
                index_best_candidate = index_candidate

        return index_best_candidate