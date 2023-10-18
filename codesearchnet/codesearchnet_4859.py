def _find_nearest_cluster(self, point):
        """!
        @brief Find nearest cluster to the specified point.

        @param[in] point (list): Point from dataset.

        @return (uint, double) Index of nearest cluster and distance to it.

        """
        index_cluster = -1;
        nearest_distance = float('inf');

        for index in range(len(self._representatives)):
            distance = self._metric(point, self._representatives[index]);
            if distance < nearest_distance:
                index_cluster = index;
                nearest_distance = distance;

        return index_cluster, nearest_distance;