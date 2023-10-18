def append_clusters(self, clusters, data=None, marker='.', markersize=None):
        """!
        @brief Appends list of cluster for visualization.

        @param[in] clusters (list): List of clusters where each cluster may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] marker (string): Marker that is used for displaying objects from clusters on the canvas.
        @param[in] markersize (uint): Size of marker.

        """

        for cluster in clusters:
            self.append_cluster(cluster, data, marker, markersize)