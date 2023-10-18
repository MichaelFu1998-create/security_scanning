def __local_to_global_clusters(self, local_clusters, available_indexes):
        """!
        @brief Converts clusters in local region define by 'available_indexes' to global clusters.

        @param[in] local_clusters (list): Local clusters in specific region.
        @param[in] available_indexes (list): Map between local and global point's indexes.

        @return Global clusters.

        """

        clusters = []
        for local_cluster in local_clusters:
            current_cluster = []
            for index_point in local_cluster:
                current_cluster.append(available_indexes[index_point])

            clusters.append(current_cluster)

        return clusters