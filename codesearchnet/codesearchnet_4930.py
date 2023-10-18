def __process_by_python(self):
        """!
        @brief Performs cluster analysis using python code.

        """

        maximum_change = float('inf')
        iteration = 0

        if self.__observer is not None:
            initial_clusters = self.__update_clusters()
            self.__observer.notify(initial_clusters, self.__centers.tolist())

        while maximum_change > self.__tolerance and iteration < self.__itermax:
            self.__clusters = self.__update_clusters()
            updated_centers = self.__update_centers()  # changes should be calculated before assignment

            if self.__observer is not None:
                self.__observer.notify(self.__clusters, updated_centers.tolist())

            maximum_change = self.__calculate_changes(updated_centers)

            self.__centers = updated_centers    # assign center after change calculation
            iteration += 1

        self.__calculate_total_wce()