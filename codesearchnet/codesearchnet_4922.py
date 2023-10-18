def __process_by_python(self):
        """!
        @brief Performs processing using python code.

        """
        self.__scores = {}

        for k in range(self.__kmin, self.__kmax):
            clusters = self.__calculate_clusters(k)
            if len(clusters) != k:
                self.__scores[k] = float('nan')
                continue

            score = silhouette(self.__data, clusters).process().get_score()

            self.__scores[k] = sum(score) / len(score)

            if self.__scores[k] > self.__score:
                self.__score = self.__scores[k]
                self.__amount = k