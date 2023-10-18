def append_cluster(self, cluster, data = None, marker = '.', markersize = None, color = None):
        """!
        @brief Appends cluster for visualization.

        @param[in] cluster (list): cluster that may consist of indexes of objects from the data or object itself.
        @param[in] data (list): If defines that each element of cluster is considered as a index of object from the data.
        @param[in] marker (string): Marker that is used for displaying objects from cluster on the canvas.
        @param[in] markersize (uint): Size of marker.
        @param[in] color (string): Color of marker.

        @return Returns index of cluster descriptor on the canvas.

        """
        if len(cluster) == 0:
            raise ValueError("Empty cluster is provided.")

        markersize = markersize or 5
        if color is None:
            index_color = len(self.__clusters) % len(color_list.TITLES)
            color = color_list.TITLES[index_color]

        cluster_descriptor = canvas_cluster_descr(cluster, data, marker, markersize, color)
        self.__clusters.append(cluster_descriptor)